---
layout: post
title: "[OpenNMT]训练模块源码剖析"
excerpt: "讨论训练模块的相关设计"
date: 2018-12-17 18:43:00
mathjax: true
---

[预处理模块代码剖析](https://zhpmatrix.github.io/2018/12/17/opennmt-source-code-reading-0/)已经梳理过了，建议在读这篇博客前先浏览一下预处理模块的文章。

本部分是OpenNMT最大的模块，也是OpenNMT的核心。**OpenNMT-py的参数共有100+**，其中最多的参数也是集中在该部分，通过给train.py传递不同的参数，可以搭建各种各样的模型，简而言之，“只用参数搭模型”。

调用下述命令，开始训练：

    python train.py -world_size 1 -gpu_ranks 0 -data data/demo -train_steps 200 -save_model demo-model

上述命令会进入train.py中，具体路径：OpenNMT/train.py。该文件主要包括两块逻辑，第一设备选择和GPU多卡处理；第二进程错误捕获。进程错误捕获是服务于GPU多卡处理的。当训练在多张卡上进行的时候，创建进程队列(torch.multiprocessing)，同时用进程错误捕获器(ErrorHandler)监控队列。逻辑组织如下：

```

    nb_gpu = len(opt.gpu_ranks)

    if opt.world_size > 1:
        mp = torch.multiprocessing.get_context('spawn')
        # Create a thread to listen for errors in the child processes.
        error_queue = mp.SimpleQueue()
        error_handler = ErrorHandler(error_queue)
        # Train with multiprocessing.
        procs = []
        for device_id in range(nb_gpu):
            procs.append(mp.Process(target=run, args=(
                opt, device_id, error_queue, ), daemon=True))
            procs[device_id].start()
            logger.info(" Starting process pid: %d  " % procs[device_id].pid)
            error_handler.add_child(procs[device_id].pid)
        for p in procs:
            p.join()

    elif nb_gpu == 1:  # case 1 GPU only
        single_main(opt, 0)
    else:   # case only CPU
        single_main(opt, -1)

```

从上述代码可以看到，

if语句是GPU多卡处理，简而言之，每块GPU处理一个进程；

elif是单卡GPU处理，相比前者，代码显得清爽很多，不需要初始化和错误捕获，多进程本来就是个大问题；

else是CPU处理。

针对if中的逻辑，提一个有趣的问题，**如何为OpenNMT添加单机跨卡BatchNorm的逻辑代码？**

j按图索骥，进入single_main函数看一下核心逻辑。该函数的逻辑在OpenNMT-py/onmt/train_single.py中，该函数接受的参数包括两个：客户端传入的参数和设备号。train_single.py给出了模型训练整个生命周期的过程：

1.判断是否需要加载checkpoint？如果需要，加载；不需要，设置checkpoint=None；

2.加载数据；

3.构建模型，build_model(model\_opt, opt, fields, checkpoint)；

4.构建优化器，build_optim(model，opt，checkpoint)；

5.构建模型保存器，build_model_saver(...)；

6.构建训练器，build_trainer(...)；

7.开始训练；

8.训练结束，如果TensorBoard开着，则关闭TensorBoard；

核心代码如下(清理掉一些logging代码，不影响对核心逻辑的理解)：

```

def main(opt, device_id):
    opt = training_opt_postprocessing(opt, device_id)
    # Load checkpoint if we resume from a previous training.
    if opt.train_from:
        checkpoint = torch.load(opt.train_from,
                                map_location=lambda storage, loc: storage)
        model_opt = checkpoint['opt']
    else:
        checkpoint = None
        model_opt = opt

    # Peek the first dataset to determine the data_type.
    # (All datasets have the same data_type).
    first_dataset = next(lazily_load_dataset("train", opt))
    data_type = first_dataset.data_type

    # Load fields generated from preprocess phase.
    fields = _load_fields(first_dataset, data_type, opt, checkpoint)

    # Report src/tgt features.

    src_features, tgt_features = _collect_report_features(fields)
    
    # Build model.
    model = build_model(model_opt, opt, fields, checkpoint)
    n_params, enc, dec = _tally_parameters(model)
    _check_save_model_path(opt)

    # Build optimizer.
    optim = build_optim(model, opt, checkpoint)

    # Build model saver
    model_saver = build_model_saver(model_opt, opt, model, fields, optim)

    trainer = build_trainer(opt, device_id, model, fields,
                            optim, data_type, model_saver=model_saver)

    def train_iter_fct(): return build_dataset_iter(
        lazily_load_dataset("train", opt), fields, opt)

    def valid_iter_fct(): return build_dataset_iter(
        lazily_load_dataset("valid", opt), fields, opt, is_train=False)

    trainer.train(train_iter_fct, valid_iter_fct, opt.train_steps,
                  opt.valid_steps)

    if opt.tensorboard:
        trainer.report_manager.tensorboard_writer.close()
```

也就是说，上述代码描述了训练过程的一个生命周期。上文中关于设备选择和并行化处理的逻辑是第一层抽象，生命周期的描述是第二层抽象，那么具体的实现就是第三层抽象了，也就是模型是怎么构建的，优化器是怎么构建的，模型和优化器都很多，又是如何组织的？

#### 构建模型

构建模型的实现在OpenNMT-py/onmt/model_builder.py中，核心逻辑围绕下面一行代码完成，
    
    model=onmt.models.NMTModel(encoder,decoder)

主要处理的逻辑包括，不同的数据类型对应不同的encoder方式；embedding的不同使用方式，预训练或者随机初始化，是否共享；部分NMT相关Trick(如copy的实现)等。从引入的模块，可见一斑，

```
from onmt.encoders.rnn_encoder import RNNEncoder
from onmt.encoders.transformer import TransformerEncoder
from onmt.encoders.cnn_encoder import CNNEncoder
from onmt.encoders.mean_encoder import MeanEncoder
from onmt.encoders.audio_encoder import AudioEncoder
from onmt.encoders.image_encoder import ImageEncoder

from onmt.decoders.decoder import InputFeedRNNDecoder, StdRNNDecoder
from onmt.decoders.transformer import TransformerDecoder
from onmt.decoders.cnn_decoder import CNNDecoder

from onmt.modules import Embeddings, CopyGenerator

```

也即是说，该部分逻辑将模型拆解成多个组件，分为编码器，解码器，embedding，以copy机制为代表的相关Trick等。

#### 构建优化器

构架优化器的实现在OpenNMT-py/onmt/utils/optimizers.py中，该部分主要是调用PyTorch内置的优化器(torch.optim)。围绕优化器的扩展也可以做的很大，我本机的代码将该模块放在工具utils目录中，感觉优化器有点受冷落的感觉呀。不过，从另一方面来看，PyTorch的优化器扩展如果做的很好，OpenNMT中的封装确实可以做的相对薄一些，毕竟应该不需要单纯针对NMT任务的优化器设计。

#### 构建训练器

训练器执行真正的训练过程，包括参数更新，梯度回传等，代码所在路径OpenNMT-py/onmt/trainer.py。

其实，到此为止，第三层抽象已经结束。假设以使用PyTorch的内置函数为标准，也就是抽象的底层，则优化器和训练器都已经触底。但是模型层面显然尚未触底，这也是OpenNMT的特色所在，假设称之为第四层抽象吧。

在OpenNMT-py/onmt/目录下，有三个目录，分别是encoders，decoders和modules。其中，可以分别从两个层面对encoders进行分类，从**模型类型**角度，分别是CNN，RNN，Transformer；从**数据类型角度**分别是text，image，audio。每种类型的实现都是基于PyTorch重新定义了一个模型，所以需要实现初始化操作，前向操作。这里可以看到，抽象到第四层，终于触底，回到了比较熟悉的基于PyTorch定义模型的阶段。  

decoders可以分为CNN，RNN和Transformer。其中最常见的RNN作为解码端实现了InputFeedRNNDecoder，StdRNNDecoder，对应了两种训练方式，分别是teacher-forcing和non teacher-forcing。**此处抛出一个问题，怎么添加professor-forcing的训练方式？**

_提示:本机版本代码提到StdRNNDecoder目前还没有coverage和copy机制的支持！_

值得一提的是，decoder目录中给出了模型融合的实现emsemble.py!!!

长吁一口气，至此，四层抽象结束，训练过程的主要逻辑也整理通顺了。还有一些边角的东西没有提到，比如由于RNN/CNN的多样性，用工厂模式来组织，但是由于目前类型受限，虽然代码中体现了，但是逻辑还没有写的很大，所以暂时不提。相关评估指标的实现，例如困惑度等。


总结一下，总共有四层抽象，其实也可以没有第四层。如下，

第一层：设备判断和并行处理；

第二层：生命周期描述；

第三层：优化器，训练器等组件实现；

第四层：模型组件实现；

利用Python的抽象，封装，继承等特性，实现了四层的模块组织结构，具有良好的扩展性。虽然，个人认为架构上尚不完美，但是已经可以学到很多了。在实现一个新的Trick或者组件的时候，需要能够走通四层抽象并按照架构设计来完成，比如父类继承等。有了清晰的抽象层次，自顶向下实现和自底向上实现都是可行的。另一方面，通过梳理架构，也看到了很多需要继续完善的地方。

除了预处理和训练模块，还有一个模块是翻译模块，入口代码是**translate.py**，这块内容较少，不准备单开一篇博客来写。从整体上看，translate.py中实现了三部分的逻辑，第一是translate的入口逻辑，第二是batch条件下的translate，第三是评估指标报告，包括score、bleu和rouge等。

其中batch条件下的translate实现源码中给出了详细的注释，步骤包括准备search组件，src通过encoder，重复beam\_size次src，使用beam\_search运行decoder生成句子，从beam中提取句子。

需要注意的是，一些特殊Trick的实现例如copy机制等，需要在解码端有配合实现。所以，如果有修改源码的需求，主要同时处理预处理模块和翻译模块。


此外，值得提到的一点是，多用公认的第三方评测工具。例如，

```
def _report_bleu(self, tgt_path):
        import subprocess
        base_dir = os.path.abspath(__file__ + "/../../..")
        # Rollback pointer to the beginning.
        self.out_file.seek(0)
        print()

        res = subprocess.check_output("perl %s/tools/multi-bleu.perl %s"
                                      % (base_dir, tgt_path),
                                      stdin=self.out_file,
                                      shell=True).decode("utf-8")

        msg = ">> " + res.strip()
        return msg

    def _report_rouge(self, tgt_path):
        import subprocess
        path = os.path.split(os.path.realpath(__file__))[0]
        res = subprocess.check_output(
            "python %s/tools/test_rouge.py -r %s -c STDIN"
            % (path, tgt_path),
            shell=True,
            stdin=self.out_file).decode("utf-8")
        msg = res.strip()
        return msg
```

总结：通过两篇博客梳理了OpenNMT-py的代码架构，对自己来说，大概有三方面的意义，第一是学习架构。涉及到抽象，接口，继承，层次等概念；第二是能够有机会基于OpenNMT-py的源码实现一些想法，框架使用是浅层的意义，更重要的是能够基于框架做代码的二次开发；第三是能够从OpenNMT-py中学习到一些实现上的启发可以用到OpenNMT-tf等框架上。

就这样，回去洗澡了。
