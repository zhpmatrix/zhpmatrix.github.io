---
layout: post
title: "[tensor2tensor源码阅读]目录结构和部分重点参数讨论"
excerpt: "去年对比opennmt-py和tensor2tensor，但是只是写了opennmt-py的源码结构，并没有梳理tensor2tensor的结构，最近刚好重启一个大实验，组里同学也在做相关的事情，因此借此机会重新梳理一些关于tensor2tensor的内容。"
date: 2019-04-23 18:43:00
mathjax: true
---

<script type="text/javascript" src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=default"></script>

### 一.前言

为了简化描述，后续均使用t2t来代替tensor2tensor。比起pytorch这类通用型框架，tensor2tensor其实文档写的并不算很清晰，因此有些部分需要回到代码中，看注释，看代码逻辑来理解。幸运的是tensor2tensor的架构还是很清晰的，因此有必要写点东西以做记录。

### 二.源码结构

进入tensor2tensor的根目录，首先要去的是bin目录，所有能够在命令行中看到的命令，都可以在该目录文件夹下看到。个人常用的是t2t\_datagen, t2t\_trainer, t2t\_decoder, t2t\_avg\_all，其余的包括：t2t\_distill, t2t\_prune,t2t\_bleu, t2t\_attack等应该在对应场景下用途很广。其中，t2t\_prune的代码中注释道：

```
This supports a very common form of pruning known as magnitude-based pruning.
It ranks individual weights or units according to their magnitudes and zeros
out the smallest k% of weights, effectively removing them from the graph.


```

这样对t2t可以做什么就有了一个基本的认识了，接下来当然要去**数据层**了，来到data\_generator目录下。t2t中对于数据的处理定义为**‘problem’**，因此当我们需要处理自己的数据时，通常需要写一个problem类。t2t的发展很快，相比于去年，problem已经积累了很多，这里可以查看[所有的problem](https://github.com/tensorflow/tensor2tensor/blob/master/tensor2tensor/data_generators/all_problems.py)。但是t2t可以处理的数据模态还是文本，声音，图片等。这个模块的架构还是非常清晰的，后续有需要处理多种数据的情形可以参照这块的代码逻辑。

有了数据，之后就需要选择模型了，这个时候可以直接来到**models文件夹**中了。依据处理模态的不同，依然有不同的模型实现，包括lstm/transformer/resnet/gan等。在实现模型的时候，必然需要对layer进行封装，因此可以到layers目录下查看各种layer的实现。有一类模型相对特殊，也就是增强学习，因此相关实现放在了rl单独一个目录中。

有了数据，有了模型，可以开始训练了。来到**utils目录**中，这里包含了metric逻辑，训练逻辑，优化逻辑等，这些模块对于不同的problem都是相同的，因此在t2t的封装中，将这些模块都封装成了工具类。

调试transformer模型的一个**flask前端**，在单独的一个insights目录中，一般情况下在部署模型之前，会做一个本地前端进行测试，这样自己就不需要搭前端了。与之相关的是visualization和serving两个模块，分别对应attention的可视化和模型部署。

最后，**mesh\_tensorflow**放置了一些关于分布式应用的例子。

### 三.重点参数

t2t通过命令行的方式给出了我们一个指定参数的机会，同时tensortensor2tensor/tensor2tensor/layers/common\_hparams.py中存放了默认参数。

1.batch\_size

对于t2t_trainer来说，也就是在模型训练时候的batch\_size，代码中有注释如下：

```
 # If the problem consists of variable-length sequences
      # (see problem.batch_size_means_tokens()), then this is the number
      # of tokens per batch per GPU or per TPU core.  Otherwise, this is
      # the number of examples per GPU or per TPU core.
      batch_size=4096,
```

也就是说默认的batch\_size根据条件的不同，可以表示两种含义。

第一：如果指定了problem.batch\_size\_means\_tokens()=True，则表示每个gpu的每个batch处理的tokens；实际上，通过读源代码可以知道，这也是t2t支持且默认的设置。

第二：如果不指定上述参数，则表示每个gpu处理的examples；其实这种情况是我们所熟悉的一种场景，在等长序列场景下，使用起来就比较顺畅了。但是如果可变长度序列场景下，这种情形对应了多数场景下的nlp问题，为了提升处理效率，第一种方式可能更加合适一些。

从自己之前的经验来看，该参数影响的是gpu利用的效率，对最终结果的影响不是决定性的。但是有必要对t2t中基于token的batch机制进一步理解。

不过batch\_size这个参数不仅在trainer中出现，同样在decoder中出现。看代码如下（该代码出现在utils/trainer\_lib.py中）：

```
def create_estimator(model_name,
                     hparams,
                     run_config,
                     schedule="train_and_evaluate",
                     decode_hparams=None,
                     use_tpu=False,
                     use_tpu_estimator=False,
                     use_xla=False):
  """Create a T2T Estimator."""
  model_fn = t2t_model.T2TModel.make_estimator_model_fn(
      model_name, hparams, decode_hparams=decode_hparams)

  del use_xla
  if use_tpu or use_tpu_estimator:
    problem = hparams.problem
    batch_size = (
        problem.tpu_batch_size_per_shard(hparams) *
        run_config.tpu_config.num_shards)
    if getattr(hparams, "mtf_mode", False):
      batch_size = problem.tpu_batch_size_per_shard(hparams)
    predict_batch_size = batch_size
    if decode_hparams and decode_hparams.batch_size:
      predict_batch_size = decode_hparams.batch_size
    estimator = tf.contrib.tpu.TPUEstimator(
        model_fn=model_fn,
        model_dir=run_config.model_dir,
        config=run_config,
        use_tpu=use_tpu,
        train_batch_size=batch_size,
        eval_batch_size=batch_size if "eval" in schedule else None,
        predict_batch_size=predict_batch_size)
  else:
    estimator = tf.estimator.Estimator(
        model_fn=model_fn,
        model_dir=run_config.model_dir,
        config=run_config,
    )
  return estimator

```

由此推测，对于eval来说，train和eval的batch\_size的含义相同，但是对于decode阶段来说，对应的batch\_size应该就是样本个数。



2.max\_subtoken\_length

在tensor2tensor/data\_generators/text\_problems.py中，关于该参数的代码如下：

```
@property
  def max_subtoken_length(self):
    """Maximum subtoken length when generating vocab.
    SubwordTextEncoder vocabulary building is quadratic-time wrt this variable,
    setting it to None uses the length of the longest token in the corpus.
    Returns:
      an integer or None
    """
    return 200

```

tensor2tensor默认使用subword方式来做tokenization，那么这里面就会遇到最长token的问题，如果将该参数设置为None，则表示使用最长的token；但是如果设定为一个值，则表示最长的token就是该值。关于该参数还没有来得及去读代码，该参数是作用于vocab构建过程中，还是构建之后的后处理操作，不过单纯从注释来看，是前者。放在纠错任务中，我目前的该值设定为10，虽然默认值是200，但是结合自己的场景，其实还是过长的。

3.clip\_grad\_norm

tensortensor2tensor/tensor2tensor/layers/common\_hparams.py中存放了该参数值，默认值为2.0。

4.max\_length

```
 	# During training, we drop sequences whose inputs or targets are longer
      # than max_length.
      # If max_length==0, we use hparams.batch_size instead.
      max_length=0,
      # Maximum length in the smallest length bucket.  Setting this
      # flag too high will result in wasteful padding of short
      # sequences.  Due to some (hopefully) temporary hacks in the
      # data reading and batching code, setting this flag too low
      # results in a very long batch-shuffling queue.
```

### 四.重要文章

《Training Tips for the Transformer Model》,[阅读笔记这里](https://github.com/zhpmatrix/reading-notes/blob/master/论文.md)



### 附录(tensor2tensor 1.9.0的源码结构)

```
.
├── bin
│   ├── build_vocab.py
│   ├── __init__.py
│   ├── make_tf_configs.py
│   ├── __pycache__
│   │   ├── build_vocab.cpython-36.pyc
│   │   ├── __init__.cpython-36.pyc
│   │   ├── make_tf_configs.cpython-36.pyc
│   │   ├── t2t_attack.cpython-36.pyc
│   │   ├── t2t_avg_all.cpython-36.pyc
│   │   ├── t2t_bleu.cpython-36.pyc
│   │   ├── t2t_datagen.cpython-36.pyc
│   │   ├── t2t_decoder.cpython-36.pyc
│   │   ├── t2t_distill.cpython-36.pyc
│   │   ├── t2t_prune.cpython-36.pyc
│   │   ├── t2t_trainer.cpython-36.pyc
│   │   ├── t2t_trainer_test.cpython-36.pyc
│   │   └── t2t_translate_all.cpython-36.pyc
│   ├── t2t_attack.py
│   ├── t2t_avg_all.py
│   ├── t2t_bleu.py
│   ├── t2t_datagen.py
│   ├── t2t_decoder.py
│   ├── t2t_distill.py
│   ├── t2t_prune.py
│   ├── t2t_trainer.py
│   ├── t2t_trainer_test.py
│   └── t2t_translate_all.py
├── data_generators
│   ├── algorithmic_math.py
│   ├── algorithmic_math_test.py
│   ├── algorithmic.py
│   ├── algorithmic_test.py
│   ├── allen_brain.py
│   ├── allen_brain_test.py
│   ├── all_problems.py
│   ├── audio_encoder.py
│   ├── audio.py
│   ├── audio_test.py
│   ├── babi_qa.py
│   ├── bair_robot_pushing.py
│   ├── celebahq.py
│   ├── celeba.py
│   ├── celeba_test.py
│   ├── cifar.py
│   ├── cipher.py
│   ├── cnn_dailymail.py
│   ├── cola.py
│   ├── common_voice.py
│   ├── common_voice_test.py
│   ├── desc2code.py
│   ├── desc2code_test.py
│   ├── dna_encoder.py
│   ├── dna_encoder_test.py
│   ├── fsns.py
│   ├── function_docstring.py
│   ├── gene_expression.py
│   ├── gene_expression_test.py
│   ├── generator_utils.py
│   ├── generator_utils_test.py
│   ├── google_robot_pushing.py
│   ├── gym_problems.py
│   ├── gym_problems_specs.py
│   ├── gym_problems_test.py
│   ├── gym_utils.py
│   ├── ice_parsing.py
│   ├── image_lsun.py
│   ├── imagenet.py
│   ├── imagenet_test.py
│   ├── image_utils.py
│   ├── image_utils_test.py
│   ├── imdb.py
│   ├── __init__.py
│   ├── inspect_tfrecord.py
│   ├── lambada.py
│   ├── librispeech.py
│   ├── lm1b_imdb.py
│   ├── lm1b_mnli.py
│   ├── lm1b.py
│   ├── mnist.py
│   ├── mrpc.py
│   ├── mscoco.py
│   ├── mscoco_test.py
│   ├── multinli.py
│   ├── multi_problem.py
│   ├── ocr.py
│   ├── paraphrase_ms_coco.py
│   ├── paraphrase_ms_coco_test.py
│   ├── pointer_generator_word.py
│   ├── problem_hparams.py
│   ├── problem.py
│   ├── problem_test.py
│   ├── program_search.py
│   ├── program_search_test.py
│   ├── ptb.py
│   ├── __pycache__
│   │   ├── algorithmic.cpython-36.pyc
│   │   ├── algorithmic_math.cpython-36.pyc
│   │   ├── algorithmic_math_test.cpython-36.pyc
│   │   ├── algorithmic_test.cpython-36.pyc
│   │   ├── allen_brain.cpython-36.pyc
│   │   ├── allen_brain_test.cpython-36.pyc
│   │   ├── all_problems.cpython-36.pyc
│   │   ├── audio.cpython-36.pyc
│   │   ├── audio_encoder.cpython-36.pyc
│   │   ├── audio_test.cpython-36.pyc
│   │   ├── babi_qa.cpython-36.pyc
│   │   ├── bair_robot_pushing.cpython-36.pyc
│   │   ├── celeba.cpython-36.pyc
│   │   ├── celebahq.cpython-36.pyc
│   │   ├── celeba_test.cpython-36.pyc
│   │   ├── cifar.cpython-36.pyc
│   │   ├── cipher.cpython-36.pyc
│   │   ├── cnn_dailymail.cpython-36.pyc
│   │   ├── cola.cpython-36.pyc
│   │   ├── common_voice.cpython-36.pyc
│   │   ├── common_voice_test.cpython-36.pyc
│   │   ├── desc2code.cpython-36.pyc
│   │   ├── desc2code_test.cpython-36.pyc
│   │   ├── dna_encoder.cpython-36.pyc
│   │   ├── dna_encoder_test.cpython-36.pyc
│   │   ├── fsns.cpython-36.pyc
│   │   ├── function_docstring.cpython-36.pyc
│   │   ├── gene_expression.cpython-36.pyc
│   │   ├── gene_expression_test.cpython-36.pyc
│   │   ├── generator_utils.cpython-36.pyc
│   │   ├── generator_utils_test.cpython-36.pyc
│   │   ├── google_robot_pushing.cpython-36.pyc
│   │   ├── gym_problems.cpython-36.pyc
│   │   ├── gym_problems_specs.cpython-36.pyc
│   │   ├── gym_problems_test.cpython-36.pyc
│   │   ├── gym_utils.cpython-36.pyc
│   │   ├── ice_parsing.cpython-36.pyc
│   │   ├── image_lsun.cpython-36.pyc
│   │   ├── imagenet.cpython-36.pyc
│   │   ├── imagenet_test.cpython-36.pyc
│   │   ├── image_utils.cpython-36.pyc
│   │   ├── image_utils_test.cpython-36.pyc
│   │   ├── imdb.cpython-36.pyc
│   │   ├── __init__.cpython-36.pyc
│   │   ├── inspect_tfrecord.cpython-36.pyc
│   │   ├── lambada.cpython-36.pyc
│   │   ├── librispeech.cpython-36.pyc
│   │   ├── lm1b.cpython-36.pyc
│   │   ├── lm1b_imdb.cpython-36.pyc
│   │   ├── lm1b_mnli.cpython-36.pyc
│   │   ├── mnist.cpython-36.pyc
│   │   ├── mrpc.cpython-36.pyc
│   │   ├── mscoco.cpython-36.pyc
│   │   ├── mscoco_test.cpython-36.pyc
│   │   ├── multinli.cpython-36.pyc
│   │   ├── multi_problem.cpython-36.pyc
│   │   ├── ocr.cpython-36.pyc
│   │   ├── paraphrase_ms_coco.cpython-36.pyc
│   │   ├── paraphrase_ms_coco_test.cpython-36.pyc
│   │   ├── pointer_generator_word.cpython-36.pyc
│   │   ├── problem.cpython-36.pyc
│   │   ├── problem_hparams.cpython-36.pyc
│   │   ├── problem_test.cpython-36.pyc
│   │   ├── program_search.cpython-36.pyc
│   │   ├── program_search_test.cpython-36.pyc
│   │   ├── ptb.cpython-36.pyc
│   │   ├── qnli.cpython-36.pyc
│   │   ├── quora_qpairs.cpython-36.pyc
│   │   ├── rte.cpython-36.pyc
│   │   ├── snli.cpython-36.pyc
│   │   ├── speech_recognition.cpython-36.pyc
│   │   ├── squad.cpython-36.pyc
│   │   ├── sst_binary.cpython-36.pyc
│   │   ├── stanford_nli.cpython-36.pyc
│   │   ├── style_transfer.cpython-36.pyc
│   │   ├── style_transfer_test.cpython-36.pyc
│   │   ├── subject_verb_agreement.cpython-36.pyc
│   │   ├── text_encoder_build_subword.cpython-36.pyc
│   │   ├── text_encoder.cpython-36.pyc
│   │   ├── text_encoder_test.cpython-36.pyc
│   │   ├── text_problems.cpython-36.pyc
│   │   ├── text_problems_test.cpython-36.pyc
│   │   ├── timeseries.cpython-36.pyc
│   │   ├── timeseries_data_generator.cpython-36.pyc
│   │   ├── timeseries_data_generator_test.cpython-36.pyc
│   │   ├── timeseries_test.cpython-36.pyc
│   │   ├── tokenizer.cpython-36.pyc
│   │   ├── tokenizer_test.cpython-36.pyc
│   │   ├── translate.cpython-36.pyc
│   │   ├── translate_encs.cpython-36.pyc
│   │   ├── translate_ende.cpython-36.pyc
│   │   ├── translate_enet.cpython-36.pyc
│   │   ├── translate_enfr.cpython-36.pyc
│   │   ├── translate_enid.cpython-36.pyc
│   │   ├── translate_enmk.cpython-36.pyc
│   │   ├── translate_envi.cpython-36.pyc
│   │   ├── translate_enzh.cpython-36.pyc
│   │   ├── translate_test.cpython-36.pyc
│   │   ├── twentybn.cpython-36.pyc
│   │   ├── video_generated.cpython-36.pyc
│   │   ├── video_utils.cpython-36.pyc
│   │   ├── vqa.cpython-36.pyc
│   │   ├── vqa_utils.cpython-36.pyc
│   │   ├── wiki.cpython-36.pyc
│   │   ├── wikitext103.cpython-36.pyc
│   │   ├── wnli.cpython-36.pyc
│   │   └── wsj_parsing.cpython-36.pyc
│   ├── qnli.py
│   ├── quora_qpairs.py
│   ├── rte.py
│   ├── snli.py
│   ├── speech_recognition.py
│   ├── squad.py
│   ├── sst_binary.py
│   ├── stanford_nli.py
│   ├── style_transfer.py
│   ├── style_transfer_test.py
│   ├── subject_verb_agreement.py
│   ├── test_data
│   │   ├── 1.csv
│   │   ├── corpus-1.txt
│   │   ├── corpus-2.txt
│   │   ├── vocab-1.txt
│   │   └── vocab-2.txt
│   ├── text_encoder_build_subword.py
│   ├── text_encoder.py
│   ├── text_encoder_test.py
│   ├── text_problems.py
│   ├── text_problems_test.py
│   ├── timeseries_data_generator.py
│   ├── timeseries_data_generator_test.py
│   ├── timeseries.py
│   ├── timeseries_test.py
│   ├── tokenizer.py
│   ├── tokenizer_test.py
│   ├── translate_encs.py
│   ├── translate_ende.py
│   ├── translate_enet.py
│   ├── translate_enfr.py
│   ├── translate_enid.py
│   ├── translate_enmk.py
│   ├── translate_envi.py
│   ├── translate_enzh.py
│   ├── translate.py
│   ├── translate_test.py
│   ├── twentybn.py
│   ├── video_generated.py
│   ├── video_utils.py
│   ├── vqa.py
│   ├── vqa_utils.py
│   ├── wiki.py
│   ├── wikisum
│   │   ├── generate_vocab.py
│   │   ├── get_references_commoncrawl.py
│   │   ├── get_references_web.py
│   │   ├── get_references_web_single_group.py
│   │   ├── html.py
│   │   ├── __init__.py
│   │   ├── parallel_launch.py
│   │   ├── produce_examples.py
│   │   ├── __pycache__
│   │   │   ├── generate_vocab.cpython-36.pyc
│   │   │   ├── get_references_commoncrawl.cpython-36.pyc
│   │   │   ├── get_references_web.cpython-36.pyc
│   │   │   ├── get_references_web_single_group.cpython-36.pyc
│   │   │   ├── html.cpython-36.pyc
│   │   │   ├── __init__.cpython-36.pyc
│   │   │   ├── parallel_launch.cpython-36.pyc
│   │   │   ├── produce_examples.cpython-36.pyc
│   │   │   ├── utils.cpython-36.pyc
│   │   │   ├── utils_test.cpython-36.pyc
│   │   │   ├── validate_data.cpython-36.pyc
│   │   │   └── wikisum.cpython-36.pyc
│   │   ├── test_data
│   │   │   ├── para_bad1.txt
│   │   │   └── para_good1.txt
│   │   ├── utils.py
│   │   ├── utils_test.py
│   │   ├── validate_data.py
│   │   └── wikisum.py
│   ├── wikitext103.py
│   ├── wnli.py
│   └── wsj_parsing.py
├── __init__.py
├── insights
│   ├── graph.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── graph.cpython-36.pyc
│   │   ├── __init__.cpython-36.pyc
│   │   ├── query_processor.cpython-36.pyc
│   │   ├── server.cpython-36.pyc
│   │   └── transformer_model.cpython-36.pyc
│   ├── query_processor.py
│   ├── server.py
│   └── transformer_model.py
├── layers
│   ├── common_attention.py
│   ├── common_attention_test.py
│   ├── common_hparams.py
│   ├── common_image_attention.py
│   ├── common_image_attention_test.py
│   ├── common_layers.py
│   ├── common_layers_test.py
│   ├── common_message_passing_attention.py
│   ├── common_video.py
│   ├── common_video_test.py
│   ├── discretization.py
│   ├── discretization_test.py
│   ├── __init__.py
│   ├── latent_layers.py
│   ├── modalities.py
│   ├── modalities_test.py
│   ├── __pycache__
│   │   ├── common_attention.cpython-36.pyc
│   │   ├── common_attention_test.cpython-36.pyc
│   │   ├── common_hparams.cpython-36.pyc
│   │   ├── common_image_attention.cpython-36.pyc
│   │   ├── common_image_attention_test.cpython-36.pyc
│   │   ├── common_layers.cpython-36.pyc
│   │   ├── common_layers_test.cpython-36.pyc
│   │   ├── common_message_passing_attention.cpython-36.pyc
│   │   ├── common_video.cpython-36.pyc
│   │   ├── common_video_test.cpython-36.pyc
│   │   ├── discretization.cpython-36.pyc
│   │   ├── discretization_test.cpython-36.pyc
│   │   ├── __init__.cpython-36.pyc
│   │   ├── latent_layers.cpython-36.pyc
│   │   ├── modalities.cpython-36.pyc
│   │   ├── modalities_test.cpython-36.pyc
│   │   ├── vqa_layers.cpython-36.pyc
│   │   └── vq_discrete.cpython-36.pyc
│   ├── vqa_layers.py
│   └── vq_discrete.py
├── mesh_tensorflow
│   ├── __init__.py
│   ├── mesh_tensorflow.py
│   ├── mesh_tensorflow_test.py
│   ├── mnist_dataset.py
│   ├── mnist.py
│   ├── mtf_beam_search.py
│   ├── mtf_image_transformer.py
│   ├── mtf_image_transformer_test.py
│   ├── mtf_layers.py
│   ├── mtf_layers_test.py
│   ├── mtf_model.py
│   ├── mtf_optimize.py
│   ├── mtf_toy_model_tpu.py
│   ├── mtf_transformer.py
│   ├── mtf_transformer_test.py
│   ├── mtf_utils.py
│   ├── placement_mesh_impl.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   ├── mesh_tensorflow.cpython-36.pyc
│   │   ├── mesh_tensorflow_test.cpython-36.pyc
│   │   ├── mnist.cpython-36.pyc
│   │   ├── mnist_dataset.cpython-36.pyc
│   │   ├── mtf_beam_search.cpython-36.pyc
│   │   ├── mtf_image_transformer.cpython-36.pyc
│   │   ├── mtf_image_transformer_test.cpython-36.pyc
│   │   ├── mtf_layers.cpython-36.pyc
│   │   ├── mtf_layers_test.cpython-36.pyc
│   │   ├── mtf_model.cpython-36.pyc
│   │   ├── mtf_optimize.cpython-36.pyc
│   │   ├── mtf_toy_model_tpu.cpython-36.pyc
│   │   ├── mtf_transformer.cpython-36.pyc
│   │   ├── mtf_transformer_test.cpython-36.pyc
│   │   ├── mtf_utils.cpython-36.pyc
│   │   ├── placement_mesh_impl.cpython-36.pyc
│   │   ├── simd_mesh_impl.cpython-36.pyc
│   │   └── tpu_variables.cpython-36.pyc
│   ├── research
│   │   ├── experiments_moe.py
│   │   ├── __init__.py
│   │   ├── moe.py
│   │   └── __pycache__
│   │       ├── experiments_moe.cpython-36.pyc
│   │       ├── __init__.cpython-36.pyc
│   │       └── moe.cpython-36.pyc
│   ├── simd_mesh_impl.py
│   └── tpu_variables.py
├── models
│   ├── basic.py
│   ├── basic_test.py
│   ├── bytenet.py
│   ├── bytenet_test.py
│   ├── distillation.py
│   ├── image_transformer_2d.py
│   ├── image_transformer_2d_test.py
│   ├── image_transformer.py
│   ├── image_transformer_test.py
│   ├── __init__.py
│   ├── lstm.py
│   ├── lstm_test.py
│   ├── neural_gpu.py
│   ├── neural_gpu_test.py
│   ├── __pycache__
│   │   ├── basic.cpython-36.pyc
│   │   ├── basic_test.cpython-36.pyc
│   │   ├── bytenet.cpython-36.pyc
│   │   ├── bytenet_test.cpython-36.pyc
│   │   ├── distillation.cpython-36.pyc
│   │   ├── image_transformer_2d.cpython-36.pyc
│   │   ├── image_transformer_2d_test.cpython-36.pyc
│   │   ├── image_transformer.cpython-36.pyc
│   │   ├── image_transformer_test.cpython-36.pyc
│   │   ├── __init__.cpython-36.pyc
│   │   ├── lstm.cpython-36.pyc
│   │   ├── lstm_test.cpython-36.pyc
│   │   ├── neural_gpu.cpython-36.pyc
│   │   ├── neural_gpu_test.cpython-36.pyc
│   │   ├── resnet.cpython-36.pyc
│   │   ├── resnet_test.cpython-36.pyc
│   │   ├── revnet.cpython-36.pyc
│   │   ├── revnet_test.cpython-36.pyc
│   │   ├── shake_shake.cpython-36.pyc
│   │   ├── slicenet.cpython-36.pyc
│   │   ├── slicenet_test.cpython-36.pyc
│   │   ├── transformer.cpython-36.pyc
│   │   ├── transformer_test.cpython-36.pyc
│   │   ├── vanilla_gan.cpython-36.pyc
│   │   ├── xception.cpython-36.pyc
│   │   └── xception_test.cpython-36.pyc
│   ├── research
│   │   ├── adafactor_experiments.py
│   │   ├── aligned.py
│   │   ├── attention_lm_moe.py
│   │   ├── attention_lm.py
│   │   ├── autoencoders.py
│   │   ├── autoencoders_test.py
│   │   ├── cycle_gan.py
│   │   ├── gene_expression.py
│   │   ├── gene_expression_test.py
│   │   ├── glow_ops.py
│   │   ├── glow_ops_test.py
│   │   ├── glow.py
│   │   ├── glow_test.py
│   │   ├── __init__.py
│   │   ├── lm_experiments.py
│   │   ├── multimodel.py
│   │   ├── multimodel_test.py
│   │   ├── __pycache__
│   │   │   ├── adafactor_experiments.cpython-36.pyc
│   │   │   ├── aligned.cpython-36.pyc
│   │   │   ├── attention_lm.cpython-36.pyc
│   │   │   ├── attention_lm_moe.cpython-36.pyc
│   │   │   ├── autoencoders.cpython-36.pyc
│   │   │   ├── autoencoders_test.cpython-36.pyc
│   │   │   ├── cycle_gan.cpython-36.pyc
│   │   │   ├── gene_expression.cpython-36.pyc
│   │   │   ├── gene_expression_test.cpython-36.pyc
│   │   │   ├── glow.cpython-36.pyc
│   │   │   ├── glow_ops.cpython-36.pyc
│   │   │   ├── glow_ops_test.cpython-36.pyc
│   │   │   ├── glow_test.cpython-36.pyc
│   │   │   ├── __init__.cpython-36.pyc
│   │   │   ├── lm_experiments.cpython-36.pyc
│   │   │   ├── multimodel.cpython-36.pyc
│   │   │   ├── multimodel_test.cpython-36.pyc
│   │   │   ├── rl.cpython-36.pyc
│   │   │   ├── similarity_transformer.cpython-36.pyc
│   │   │   ├── super_lm.cpython-36.pyc
│   │   │   ├── transformer_aux.cpython-36.pyc
│   │   │   ├── transformer_aux_test.cpython-36.pyc
│   │   │   ├── transformer_moe.cpython-36.pyc
│   │   │   ├── transformer_nat.cpython-36.pyc
│   │   │   ├── transformer_revnet.cpython-36.pyc
│   │   │   ├── transformer_revnet_test.cpython-36.pyc
│   │   │   ├── transformer_sketch.cpython-36.pyc
│   │   │   ├── transformer_symshard.cpython-36.pyc
│   │   │   ├── transformer_vae.cpython-36.pyc
│   │   │   ├── transformer_vae_test.cpython-36.pyc
│   │   │   ├── universal_transformer.cpython-36.pyc
│   │   │   ├── universal_transformer_test.cpython-36.pyc
│   │   │   ├── universal_transformer_util.cpython-36.pyc
│   │   │   ├── vqa_attention.cpython-36.pyc
│   │   │   ├── vqa_attention_test.cpython-36.pyc
│   │   │   ├── vqa_recurrent_self_attention.cpython-36.pyc
│   │   │   └── vqa_self_attention.cpython-36.pyc
│   │   ├── rl.py
│   │   ├── similarity_transformer.py
│   │   ├── super_lm.py
│   │   ├── transformer_aux.py
│   │   ├── transformer_aux_test.py
│   │   ├── transformer_moe.py
│   │   ├── transformer_nat.py
│   │   ├── transformer_revnet.py
│   │   ├── transformer_revnet_test.py
│   │   ├── transformer_sketch.py
│   │   ├── transformer_symshard.py
│   │   ├── transformer_vae.py
│   │   ├── transformer_vae_test.py
│   │   ├── universal_transformer.py
│   │   ├── universal_transformer_test.py
│   │   ├── universal_transformer_util.py
│   │   ├── vqa_attention.py
│   │   ├── vqa_attention_test.py
│   │   ├── vqa_recurrent_self_attention.py
│   │   └── vqa_self_attention.py
│   ├── resnet.py
│   ├── resnet_test.py
│   ├── revnet.py
│   ├── revnet_test.py
│   ├── shake_shake.py
│   ├── slicenet.py
│   ├── slicenet_test.py
│   ├── transformer.py
│   ├── transformer_test.py
│   ├── vanilla_gan.py
│   ├── video
│   │   ├── base_test.py
│   │   ├── base_vae.py
│   │   ├── basic_deterministic_params.py
│   │   ├── basic_deterministic.py
│   │   ├── basic_stochastic.py
│   │   ├── emily.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── base_test.cpython-36.pyc
│   │   │   ├── base_vae.cpython-36.pyc
│   │   │   ├── basic_deterministic.cpython-36.pyc
│   │   │   ├── basic_deterministic_params.cpython-36.pyc
│   │   │   ├── basic_stochastic.cpython-36.pyc
│   │   │   ├── emily.cpython-36.pyc
│   │   │   ├── __init__.cpython-36.pyc
│   │   │   ├── savp.cpython-36.pyc
│   │   │   ├── savp_params.cpython-36.pyc
│   │   │   ├── sv2p.cpython-36.pyc
│   │   │   └── sv2p_params.cpython-36.pyc
│   │   ├── savp_params.py
│   │   ├── savp.py
│   │   ├── sv2p_params.py
│   │   └── sv2p.py
│   ├── xception.py
│   └── xception_test.py
├── problems.py
├── problems_test.py
├── __pycache__
│   ├── __init__.cpython-36.pyc
│   ├── problems.cpython-36.pyc
│   └── problems_test.cpython-36.pyc
├── rl
│   ├── collect.py
│   ├── datagen_with_agent.py
│   ├── envs
│   │   ├── batch_env_factory.py
│   │   ├── batch_env.py
│   │   ├── in_graph_batch_env.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── batch_env.cpython-36.pyc
│   │   │   ├── batch_env_factory.cpython-36.pyc
│   │   │   ├── in_graph_batch_env.cpython-36.pyc
│   │   │   ├── __init__.cpython-36.pyc
│   │   │   ├── py_func_batch_env.cpython-36.pyc
│   │   │   ├── simulated_batch_env.cpython-36.pyc
│   │   │   ├── tf_atari_wrappers.cpython-36.pyc
│   │   │   └── utils.cpython-36.pyc
│   │   ├── py_func_batch_env.py
│   │   ├── simulated_batch_env.py
│   │   ├── tf_atari_wrappers.py
│   │   └── utils.py
│   ├── __init__.py
│   ├── ppo.py
│   ├── __pycache__
│   │   ├── collect.cpython-36.pyc
│   │   ├── datagen_with_agent.cpython-36.pyc
│   │   ├── __init__.cpython-36.pyc
│   │   ├── ppo.cpython-36.pyc
│   │   ├── rl_trainer_lib.cpython-36.pyc
│   │   ├── rl_trainer_lib_test.cpython-36.pyc
│   │   ├── trainer_model_based.cpython-36.pyc
│   │   ├── trainer_model_based_stochastic_test.cpython-36.pyc
│   │   ├── trainer_model_based_sv2p_test.cpython-36.pyc
│   │   ├── trainer_model_based_test.cpython-36.pyc
│   │   └── trainer_model_free.cpython-36.pyc
│   ├── rl_trainer_lib.py
│   ├── rl_trainer_lib_test.py
│   ├── trainer_model_based.py
│   ├── trainer_model_based_stochastic_test.py
│   ├── trainer_model_based_sv2p_test.py
│   ├── trainer_model_based_test.py
│   └── trainer_model_free.py
├── serving
│   ├── export.py
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── export.cpython-36.pyc
│   │   ├── __init__.cpython-36.pyc
│   │   ├── query.cpython-36.pyc
│   │   └── serving_utils.cpython-36.pyc
│   ├── query.py
│   └── serving_utils.py
├── utils
│   ├── adafactor.py
│   ├── adv_attack_utils.py
│   ├── avg_checkpoints.py
│   ├── beam_search.py
│   ├── beam_search_test.py
│   ├── bleu_hook.py
│   ├── bleu_hook_test.py
│   ├── checkpoint_compatibility_test.py
│   ├── cloud_mlengine.py
│   ├── compute_video_metrics.py
│   ├── data_reader.py
│   ├── data_reader_test.py
│   ├── decoding.py
│   ├── devices.py
│   ├── diet.py
│   ├── diet_test.py
│   ├── expert_utils.py
│   ├── expert_utils_test.py
│   ├── flags.py
│   ├── get_rouge.py
│   ├── __init__.py
│   ├── learning_rate.py
│   ├── metrics_hook.py
│   ├── metrics_hook_test.py
│   ├── metrics.py
│   ├── metrics_test.py
│   ├── modality.py
│   ├── multistep_optimizer.py
│   ├── multistep_optimizer_test.py
│   ├── optimize.py
│   ├── pruning_utils.py
│   ├── __pycache__
│   │   ├── adafactor.cpython-36.pyc
│   │   ├── adv_attack_utils.cpython-36.pyc
│   │   ├── avg_checkpoints.cpython-36.pyc
│   │   ├── beam_search.cpython-36.pyc
│   │   ├── beam_search_test.cpython-36.pyc
│   │   ├── bleu_hook.cpython-36.pyc
│   │   ├── bleu_hook_test.cpython-36.pyc
│   │   ├── checkpoint_compatibility_test.cpython-36.pyc
│   │   ├── cloud_mlengine.cpython-36.pyc
│   │   ├── compute_video_metrics.cpython-36.pyc
│   │   ├── data_reader.cpython-36.pyc
│   │   ├── data_reader_test.cpython-36.pyc
│   │   ├── decoding.cpython-36.pyc
│   │   ├── devices.cpython-36.pyc
│   │   ├── diet.cpython-36.pyc
│   │   ├── diet_test.cpython-36.pyc
│   │   ├── expert_utils.cpython-36.pyc
│   │   ├── expert_utils_test.cpython-36.pyc
│   │   ├── flags.cpython-36.pyc
│   │   ├── get_rouge.cpython-36.pyc
│   │   ├── __init__.cpython-36.pyc
│   │   ├── learning_rate.cpython-36.pyc
│   │   ├── metrics.cpython-36.pyc
│   │   ├── metrics_hook.cpython-36.pyc
│   │   ├── metrics_hook_test.cpython-36.pyc
│   │   ├── metrics_test.cpython-36.pyc
│   │   ├── modality.cpython-36.pyc
│   │   ├── multistep_optimizer.cpython-36.pyc
│   │   ├── multistep_optimizer_test.cpython-36.pyc
│   │   ├── optimize.cpython-36.pyc
│   │   ├── pruning_utils.cpython-36.pyc
│   │   ├── quantization.cpython-36.pyc
│   │   ├── registry.cpython-36.pyc
│   │   ├── registry_test.cpython-36.pyc
│   │   ├── restore_hook.cpython-36.pyc
│   │   ├── rouge.cpython-36.pyc
│   │   ├── rouge_test.cpython-36.pyc
│   │   ├── t2t_model.cpython-36.pyc
│   │   ├── t2t_model_test.cpython-36.pyc
│   │   ├── trainer_lib.cpython-36.pyc
│   │   ├── trainer_lib_test.cpython-36.pyc
│   │   ├── update_ops_hook.cpython-36.pyc
│   │   ├── usr_dir.cpython-36.pyc
│   │   ├── video2gif.cpython-36.pyc
│   │   ├── video_metrics.cpython-36.pyc
│   │   ├── yellowfin.cpython-36.pyc
│   │   └── yellowfin_test.cpython-36.pyc
│   ├── quantization.py
│   ├── registry.py
│   ├── registry_test.py
│   ├── restore_hook.py
│   ├── rouge.py
│   ├── rouge_test.py
│   ├── t2t_model.py
│   ├── t2t_model_test.py
│   ├── trainer_lib.py
│   ├── trainer_lib_test.py
│   ├── update_ops_hook.py
│   ├── usr_dir.py
│   ├── video2gif.py
│   ├── video_metrics.py
│   ├── yellowfin.py
│   └── yellowfin_test.py
└── visualization
    ├── attention.js
    ├── attention.py
    ├── __init__.py
    ├── __pycache__
    │   ├── attention.cpython-36.pyc
    │   ├── __init__.cpython-36.pyc
    │   ├── visualization.cpython-36.pyc
    │   └── visualization_test.cpython-36.pyc
    ├── TransformerVisualization.ipynb
    ├── visualization.py
    └── visualization_test.py

33 directories, 665 files

```




	





























