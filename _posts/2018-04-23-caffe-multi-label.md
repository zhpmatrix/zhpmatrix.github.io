---
layout: post
title: "Caffe修改源码支持多标签输入"
tags: [工程架构]
excerpt: "通过修改Caffe源码的方式，使得Caffe可以支持多标签输入。同时给出了一个使用Caffe进行多标签训练的例子。附带讲了如何调试Caffe的CPU和GPU版本的源代码。博客中的例子已经分享到我的Github上了，还有训练数据。"
date: 2018-04-23 15:34:00
mathjax: true
---

### Caffe的源码调试

针对Caffe的改源码的需要主要体现在支持多种数据输入格式，也就是数据层的源码修改；各种新的神经网络层的添加；各种Loss函数的添加等。一般修改源码后者添加新的层需要分别完成CPU和GPU端的代码编写，分别对应.cpp和.cu文件，当然需要.hpp和其他文件的相应支持。随着Caffe的发展，将各个Layer分开，单独形成一个文件，无论从编译还是代码维护等方面都很方便。

改源码需要调试，问了周围一些同事，他们使用printf这个万能调试语句。使用printf的优点是使用简单，缺点是灵活性差，需要反复编译。个人更喜欢gdb和cuda-gdb调试。如何做呢？

在编译Caffe源代码的时候，首先开启Debug模式。打开根目录下的Makefile.config文件，取消DEBUG := 1的注释。背后的原理是这样的，打开同目录下的Makefile文件，看到首行：

	CONFIG_FILE := Makefile.config

也是说Makefile.config是针对Makefile文件，方便配置单独拉出来的文件。当设置DEBUG := 1的时候，看到Makefile文件中的下述代码：

	ifeq($(DEBUG), 1)
		COMMON_FLAGS += -DDEBUG -g -O0
		NVCCFLAGS += -G
	else
		COMMON_FLAGS += -dedebug -O2
	endif

其中的-O0表示不进行编译优化；-O2进行编译优化；编译优化可以读一读下列的参考资料。

完整的编译参数在下行代码中体现：

	NVCCFLAGS += -ccbin=$(CXXFLAGS) -Xcompiler -fPIC $(COMMON_FLAGS)

所有，如果需要更改优化等级也是在这里。

开始调试过程，给出两篇参考文档。[调试CPU版本Caffe](https://cloud.tencent.com/developer/article/1008732), [调试GPU版本Caffe](https://blog.csdn.net/u010158659/article/details/78418701)。这里对调试过程简单梳理。

CPU调试：

	gdb --args ./build/tools/caffe train --solver=...

	b base_conv_layer.cpp:117

	r

	p variable

GPU调试：

	cuda-gdb --args ./build/tools/caffe train --solver=... --gpu 0

	start

	b pooling_layer.cu:26

	c

	p variable

需要提示的是，设置源码行的断点时，直接写layers文件夹中的layer名称就可以，不需要完整路径。

可以进行源码调试了，就可以做任何想做的事情了。有点令人激动。	

### Caffe支持多标签输入

多标签问题的应用场景是验证码识别，车牌识别等。对于每一个样本，也就是一张图片，对应多个标签，常见的是数字和26个英文字母的大小写，总共62个标签。原生Caffe是不支持多标签数据读入的，在这种场景下，可以怎么做呢？

以mnist这个example分析，输入是一张图片对应一个标签。也就是说如果能够将验证码的输入转化为和mnist的输入格式一致，问题就解决了。能够做到吗？

不要太简单。把每个验证码进行分割，得到62个标签。或者将车牌中的字符分割出来。这样做的问题是什么？

分割的速度和精度。要保证能够很好的将字符分割出来，同时要保证分割的速度。因为不仅要考虑模型训练，同时要考虑到模型部署，原问题的读入是一张完整的验证码图片，需要先分割，然后做推断。

这种方案是OK的。如果不想做分割，直接将识别做到一个完整的Pipeline呢？这就需要Caffe支持多标签读入。类似数据格式如下：

	data/train/1.jpg A 0 z 5
	data/train/2.jpg 2 B c q
	data/train/3.jpg 0 W 9 Z

假设数据读入格式是多标签的，如何去做训练呢？首先数据读入层要修改；模型结构要修改吗？Loss函数要修改吗？Metric方式要改变吗？

读取多个标签，需要标签个数的信息，且这个信息会在多个地方用到，首先声明这个参数。


在src/caffe/proto/caffe.proto中的message ImageDataParameter中添加标签个数信息。如下：

	optional unint32 label_dim = 13 [default = 1]

caffe.proto是Google Protocol Buffers中的消息格式文件定义。注意，label\_dim的值要保证和该message中的其他值不同，个人猜测，和proto的后续文件生成机制有关。caffe.proto提供了模型结构定义文件中每个层中可以使用的参数。也就是说，在这里定义label\_dim后，可以在模型结构定义文件中显式声明这个值。如果不显式声明，默认值为1，和原始版本兼容。所以，这是非常棒的一种方式。

接下来，需要修改读取的源代码了。假设这里先考虑直接读取原始图片文件的方式，也就是不考虑LMDB生成等方式。Caffe源码支持读取一个标签，那现在读取label\_dim个标签，由读取一个值，变成读取多个值。数据结构上，可能需要一个标签数组。查一下原始代码，在include/caffe/layers/image\_data\_layer.hpp中，看到这行代码：
	
	vector<std::pair<std::string, int>> lines_;

其中string应该就是图片路径，int是标签值。显然，先修改这行代码：

	vector<std::pair<std::string, int*>> lines_;

接下来自然要回到.cpp文件中，修改读取标签数组的逻辑。对应的image\_data\_layer.cpp中的函数很少，可以很容易定位到读取数据的逻辑。原始逻辑如下：

	std::ifstream infile(source.c_str());
	string line;
	size_t pos;
	int label;
	while(std::getline(infile, line)){
			pos = line.find_last_of(' ');
			//...
	}

修改为：

	std::ifstream infile(source.c_str());
	string filename;
	int lable_dim = this->layer_param_.image_data_param().label_dim();
	while(infile >> filename){
		int* labels = new int[label_dim];
		for(int i = 0;i < label_dim;++i){
			infile >> labels[i];
			}
		lines_.push_back(std::pair(filename, labels));
	}

关键代码如下：

	int lable_dim = this->layer_param_.image_data_param().label_dim();

label\_dim()就是proto生成的函数，上述过程中定义的新的变量。同时该行体现了一种调用层次和结构。

沿着读取逻辑向下看，看到这行代码：

	vector<int> label_shape(1, batch_size);

也就是说读入一个batch\_size行，1列的标签数据；对应修改如下：

	vector<int> label_shape(2);
	label_shape[0] = batch_size;
	label_shape[1] = label_dim;

上述两处修改发生在DataLayerSetup函数中，在load\_batch中，看到这行代码：

	prefetch_label[item_id] = lines_[lines_id_].second;

也要修改为读取一个标签数组，修改如下：

	int label_dim = this->layer_param_.image_data_param().label_dim();
	for(int i = 0;i < label_dim;++i){
		prefectch_label[item_id * lable_dim + 1] = lines_[lines_id_].second(i);
	}

.cpp文件应该已经修改完了，此时，可以重新编译源码。关键的问题来了，多标签数据可以直接读取了，如何训练呢？

读入的数据文件最好是标签数值化的，做一个字典映射就OK，如下：

	data/train/1.jpg 1 23 45 13
	data/train/2.jpg 2 21 22 34
	data/train/3.jpg 0 2 9 35

在博客一开始，提到一种不改变源代码的前提下的一种解决方案，就是将一张图片分割成多张图片。延续这个思路，一种网络结构定义的方式是，将读入的多个标签，也就是bottom数据，分割成多个top数据，分别优化。这也实现了博客一开始定下的目标，将分割集成进入一个统一的Pipeline中。考虑到自己整理的验证码的数据集的标签是4个，结构上是这样的。读取多标签数据，进入网络结构，分割(Slice)成四个子分支，每个分支单独进行Backbone的特征提取，Loss计算，Acc计算等。其实这也是多任务的一种典型Pipeline，如果多个任务可以进行特征迁移，可以进行任务特征的融合，也就是分支之间的运算。想想，这个地方应该会有很多有意思的idea可以去做。

给一段迭代最后的日志：

	I0423 13:45:19.216933  7692 solver.cpp:351] Iteration 10000, Testing net (#0)
	I0423 13:45:22.252681  7692 solver.cpp:418]     Test net output #0: accuracy_four = 1
	I0423 13:45:22.252704  7692 solver.cpp:418]     Test net output #1: accuracy_one = 1
	I0423 13:45:22.252710  7692 solver.cpp:418]     Test net output #2: accuracy_three = 1
	I0423 13:45:22.252715  7692 solver.cpp:418]     Test net output #3: accuracy_two = 0
	I0423 13:45:22.252722  7692 solver.cpp:418]     Test net output #4: loss_four = 0.0574376 (* 0.5 = 0.0287188 loss)
	I0423 13:45:22.252732  7692 solver.cpp:418]     Test net output #5: loss_one = 0.0573275 (* 0.5 = 0.0286638 loss)
	I0423 13:45:22.252737  7692 solver.cpp:418]     Test net output #6: loss_three = 0.0573351 (* 0.5 = 0.0286676 loss)
	I0423 13:45:22.252743  7692 solver.cpp:418]     Test net output #7: loss_two = 4.91332 (* 0.5 = 2.45666 loss)
	I0423 13:45:22.252750  7692 solver.cpp:336] Optimization Done.
	I0423 13:45:22.334941  7692 caffe.cpp:250] Optimization Done.


数据和代码参考我的Github:[Caffe多标签读入源码修改](https://github.com/zhpmatrix/Caffe_Multi_Label)


参考:

1.[GCC中-O1, -O2, -O3优化的原理是什么](https://www.zhihu.com/question/27090458)

2.[GCC编译器代码优化](http://www.cnblogs.com/21207-iHome/p/5384376.html)

针对编译优化，开发时不要优化，发布时要优化；优化要在编译速度，代码大小，执行速度之间达到一个平衡；

3.[CUDA调试的各种方法总结](https://blog.csdn.net/litdaguang/article/details/50462325)

4.[Google Protocol Buffers的一个例子](http://www.cnblogs.com/royenhome/archive/2010/10/29/1864860.html)

消息通信协议，写.prototxt文件，调用proto，生成.h和.cc文件，文件中包含get和set函数。















