```
[net]
			       
# Testing          初始batch参数要分为两类，分别为训练集和测试集，不同模式相应放开参数，#为注释符号
# batch=1
# subdivisions=1
# Training

batch=64          #一批训练样本的样本数量，每batch个样本更新一次参数
subdivisions=8    #batch/subdivisions作为一次性送入训练器的样本数量
                  #如果内存不够大，将batch分割为subdivisions个子batch
                  #subdivisions相当于分组个数，相除结果作为一次送入训练器的样本数量
				  #注意：上面这两个参数如果电脑内存小，则把batch改小一点，batch越大，训练效果越好
				  #Subdivisions越大，可以减轻显卡压力（分组数目越多，每组样本数量则会更少，显卡压力也会相应减少）
width=416           
height=416
channels=3
                  #以上三个参数为输入图像的参数信息 width和height影响网络对输入图像的分辨率，
				  #从而影响precision，只可以设置成32的倍数（为什么是32？由于使用了下采样参数是32，
				  #所以不同的尺寸大小也选择为32的倍数{320，352…..608}，最小320*320，最大608*608，网络会自动改变尺寸，并继续训练的过程。

momentum=0.9      #DeepLearning1中最优化方法中的动量参数，这个值影响着梯度下降到最优值得速度 
				  #注：SGD方法的一个缺点是其更新方向完全依赖于当前batch计算出的梯度，因而十分不稳定。Momentum算法借用了物理中的动量概念，
				  #它模拟的是物体运动时的惯性，即更新的时候在一定程度上保留之前更新的方向，同时利用当前batch的梯度微调最终的更新方向。这样一来，
				  #可以在一定程度上增加稳定性，从而学习地更快，并且还有一定摆脱局部最优的能力） 

decay=0.0005      #权重衰减正则项，防止过拟合，正则项往往有重要意义
# 数据增强
				  #增加样本的数量，改变基础样本的状态，去增加样本整体的数量，增加样本量减少过拟合
angle=0           #通过旋转角度来生成更多训练样本
saturation = 1.5  #通过调整饱和度来生成更多训练样本
exposure = 1.5    #通过调整曝光量来生成更多训练样本
hue=.1            #通过调整色调来生成更多训练样本

learning_rate=0.001 
				  #学习率决定着权值更新的速度，设置得太大会使结果超过最优值，
				  #直接错过最优值，震荡回去，太小会使下降速度过慢，导致收敛过慢。如果仅靠人为干预调整参数，需要不断修改学习率。
				  #刚开始训练时可以将学习率设置的高一点，而一定轮数之后，将其减小。在训练过程中，一般根据训练轮数设置动态变化的学习率。
				  #基本训练守则
				  #刚开始训练时：学习率以 0.01 ~ 0.001 为宜。
				  #一定轮数过后：逐渐减缓。
                  #接近训练结束：学习速率的衰减应该在100倍以上。
                  #提供参考资料学习率的调整参考https://blog.csdn.net/qq_33485434/article/details/80452941

burn_in=1000      #在迭代次数小于burn_in时，其学习率的更新有一种方式，大于burn_in时，才采用policy的更新方式

max_batches = 500200        #训练达到max_batches后停止学习，多个batches

policy=steps				
							'''
							这个是学习率调整的策略，有policy：constant, steps, exp, poly, step, sig, RANDOM，constant等方式
							调整学习率的policy，        
							有如下policy：constant, steps, exp, poly, step, sig, RANDOM
							constant#保持学习率为常量，caffe里为fixed
						    steps#比较好理解，按照steps来改变学习率
							'''


Steps和scales				#相互一一对应
steps=40000,45000       	
							'''
							下面这两个参数steps和scale是设置学习率的变化，
							比如迭代到40000次时，学习率衰减十倍。45000次迭代时，
							学习率又会在前一个学习率的基础上衰减十倍。根据batch_num调整学习率     
							'''							
scales=,.1,.1            	#学习率变化的比例，累计相乘

							#涉及几个参数（以后要学习的代码，具体参数可以调节）

exp
gamma=
							#返回base_lr*gamma^iter,iter为当前迭代次数，gamma设置为0.98

poly
power=4
max_batches=800000
							#对学习率进行多项式衰减。图中power为0.9

sig
							#学习率进行sigmod函数衰减
gamma= 0.05
step=200
							#效果如图所示


step
							#返回net.learning_rate*pow(net.scale, batch_num/net.step)

[convolutional]
batch_normalize=1    		#是否做BN操作
filters=32                  #输出特征图的数量
size=3               		#卷积核的尺寸
stride=1                	#做卷积运算的步长
pad=1               		#如果pad为0,padding由 padding参数指定。
							#如果pad为1，padding大小为size/2，padding应该是对输入图像左边缘拓展的像素数量
activation=leaky     		#激活函数的类型：logistic，loggy，relu，elu，relie，plse，hardtan，lhtan，linear，ramp，leaky，tanh，stair

# Downsample    //以下为训练网络结构。

[convolutional]
batch_normalize=1
filters=64
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=32
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=64
size=3
stride=1
pad=1
activation=leaky
shortcut				#部分是卷积的跨层连接，就像Resnet中使用的一样，
						#参数from是−3，意思是shortcut的输出是通过与先前的倒数第三层网络相加而得到。跨越连接。
[shortcut]
from=-3
activation=linear
						#输入与输出：输入与输出一般保持一致，并且不进行其他操作，只是求差。
						#处理操作：res层来源于resnet，为了解决网络的梯度弥散或者梯度爆炸的现象，
						#提出将深层神经网络的逐层训练改为逐阶段训练，将深层神经网络分为若干个子段，每个小段包含比较浅的网络层数，
						#然后用shortcut的连接方式使得每个小段对于残差进行训练，每一个小段学习总差（总的损失）的一部分，最终达到总体较小的loss，
						#同时，很好的控制梯度的传播，避免出现梯度消失或者爆炸等不利于训练的情形。

				# Downsample

[convolutional]
batch_normalize=1
filters=128
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=64
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=64
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

					# Downsample
					//	下采样
[convolutional]
batch_normalize=1
filters=256
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

				# Downsample

[convolutional]
batch_normalize=1
filters=512
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear


[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

				# Downsample

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=2
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
filters=1024
size=3
stride=1
pad=1
activation=leaky

[shortcut]
from=-3
activation=linear

				######################

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=1024
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=1024
activation=leaky

[convolutional]
batch_normalize=1
filters=512
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=1024
activation=leaky
				#**************************************重点来了*******************************************************************************
[convolutional]
size=1
stride=1
pad=1
filters=18  
							#每一个[region/yolo]层前的最后一个卷积层中的 filters=num(yolo层个数)*(classes+5) ,5的意义是5个坐标，论文中的tx,ty,tw,th,po
activation=linear


[yolo]                  	#在yoloV2中yolo层叫region层,yolo2,3各自叫法不同
mask = 6,7,8 				#训练框
mask的值是0,1,2，			#这意味着使用第一，第二和第三个anchor。 这是有道理的，因为检测层的每个单元预测3个box。 总共有三个检测层，共计9个anchor，
anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326
					'''   
					      1.anchors是可以事先通过cmd指令计算出来的，是和图片数量，width,height以及cluster
						 (应该就是下面的num的值，即想要使用的anchors的数量)相关的预选框，可以手工挑选，也可以通过k means 从训练样本中学出
						  2.聚类的脚本放在github中
						  3. 预测框的初始宽高，第一个是w，第二个是h，总数量是num*2
					'''
classes=1
num=9     			#每个grid预测的BoundingBox num/yolo层个数
jitter=.3    		'''
					利用数据抖动产生更多数据，YOLOv2中使用的是crop，filp，以及net层的angle，flip是随机的，
					crop就是jitter的参数，tiny-yolo-voc.cfg中jitter=.2，就是在0~0.2中进行cr
					'''

ignore_thresh = .5
					'''
					参数解释：ignore_thresh 指得是参与计算的IOU阈值大小。当预测的检测框与ground true的IOU大于ignore_thresh的时候，
					不会参与loss的计算，否则，检测框将会参与损失计算。
					参数目的和理解：目的是控制参与loss计算的检测框的规模，当ignore_thresh过于大，
					接近于1的时候，那么参与检测框回归loss的个数就会比较少，同时也容易造成过拟合；而如果ignore_thresh设置的过于小，
					那么参与计算的会数量规模就会很大。同时也容易在进行检测框回归的时候造成欠拟合。
					参数设置：一般选取0.5-0.7之间的一个值，之前的计算基础都是小尺度（13*13）用的是0.7，（26*26）用的是0.5。这次先将0.5更改为0.7。
					'''
truth_thresh = 1
random=1                #random设置成1，可以增加检测精度precision
   //路由层             #进行多尺度训练
[route]
layers = -4
						#当属性只有一个值时，它会输出由该值索引的网络层的特征图。 
						#在我们的示例中，它是−4，所以层级将输出路由层之前第四个层的特征图。
						#当图层有两个值时，它会返回由其值所索引的图层的连接特征图。 在我们的例子中，它是−−1,61，
						#并且该图层将输出来自上一层（-1）和第61层的特征图，并沿深度的维度连接。
[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[upsample]
stride=2

[route]
layers = -1, 61

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=512
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=512
activation=leaky

[convolutional]
batch_normalize=1
filters=256
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=512
activation=leaky

[convolutional]
size=1
stride=1
pad=1
filters=18
activation=linear


[yolo]
mask = 3,4,5
anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326
classes=1
num=9   
			'''
			每个grid cell预测几个box,和anchors的数量一致。当想要使用更多anchors时需要调大num，
			且如果调大num后训练时Obj趋近0的话可以尝试调大object_scale
			'''

jitter=.3                   
			'''
			利用数据抖动产生更多数据，YOLOv2中使用的是crop，filp，以及net层的angle，flip是随机的, 
			jitter就是crop的参数，tiny-yolo-voc.cfg中jitter=.3，就是在0~0.3中进行crop
			'''

ignore_thresh = .5  	#决定是否需要计算IOU误差的参数，大于thresh，IOU误差不会夹在cost function中
truth_thresh = 1
random=1    			#多尺度如果为1，每次迭代图片大小随机从320到608，步长为32，如果为0，每次训练大小与输入大小一致
[route]
layers = -4

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[upsample]
stride=2

[route]
layers = -1, 36



[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=256
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=256
activation=leaky

[convolutional]
batch_normalize=1
filters=128
size=1
stride=1
pad=1
activation=leaky

[convolutional]
batch_normalize=1
size=3
stride=1
pad=1
filters=256
activation=leaky

[convolutional]
size=1
stride=1
pad=1
filters=18
activation=linear


[yolo]
mask = 0,1,2
anchors = 10,13,  16,30,  33,23,  30,61,  62,45,  59,119,  116,90,  156,198,  373,326
classes=1
num=9
jitter=.3
ignore_thresh = .5
truth_thresh = 1
random=1    

	'''
	原英文地址： https://timebutt.github.io/static/understanding-yolov2-training-output/
	原中文翻译地址:https://blog.csdn.net/dcrmg/article/details/78565440 
	8个分组，因此有八个subdivision，每个subdivision有八个照片
	以上截图显示了所有训练图片的一个批次（batch），批次大小的划分根据我们在 .cfg 文件中设置的subdivisions参数。
	在我使用的 .cfg 文件中 batch = 64 ，subdivision = 8，所以在训练输出中，训练迭代包含了8组，每组又包含了8张图片，
	跟设定的batch和subdivision的值一致。（注： 也就是说每轮迭代会从所有训练集里随机抽取 batch = 64 个样本参与训练，
	所有这些 batch 个样本又被均分为 subdivision = 8 次送入网络参与训练，以减轻内存占用的压力）
	'''

•   9798： 				#指示当前训练的迭代次数
•   0.370096： 			#是总体的Loss(损失）
•   0.451929 avg：  	#是平均Loss，这个数值应该越低越好，一般来说一旦这个数值低于0.060730 avg就可以终止训练了。
•   0.001000 rate： 	#代表当前的学习率，是在.cfg文件中定义的。
•   3.300000 seconds：  #表示当前批次训练花费的总时间。
•   627072 images： 	#这一行最后的这个数值是9798*64的大小，表示到目前为止，参与训练的图片的总量。

•   Region Avg IOU: 0.326577：  #表示在当前subdivision内的图片的平均IOU，代表预测的矩形框和真实目标的交集与并集之比，这里是32.66%，这个模型需要进一步的训练。
•   Class: 0.742537： 			#标注物体分类的正确率，期望该值趋近于1。
•   Obj: 0.033966： 			#越接近1越好。
•   No Obj: 0.000793： 			#期望该值越来越小，但不为零。
•   Avg Recall: 0.12500： 		#是在recall/count中定义的，是当前模型在所有subdivision图片中检测出的正样本与实际的正样本的比值。
								#在本例中，只有八分之一的正样本被正确的检测到。（和最开始初定的阈值有关系）
•   count: 8：                  #count后的值是所有的当前subdivision图片（本例中一共8张）中包含正样本的图片的数量。
								#在输出log中的其他行中，可以看到其他subdivision也有的只含有6或7个正样本，说明在subdivision中含有不含检测对象的图片。
./darknet detector train cfg/voc.data cfg/yolov3-voc.cfg voc/ darknet53.conv.74 -gpus 0,1,2,3		#这句话的意思是采用迁移学习的权重使用4个GPU训练自己数据
--------------------- 
作者：ll_sunsmile 
来源：CSDN 
原文：https://blog.csdn.net/ll_master/article/details/81487844 
版权声明：本文为博主原创文章，转载请附上博文链接！

参考github：https://timebutt.github.io/static/understanding-yolov2-training-output/
	

yolov3有5次下采样，每次采样步长为2，网络的最大步幅为2^5=32。

（1）batchsize：批大小。在深度学习中，一般采用SGD训练，即每次训练在训练集中取batchsize个样本训练；
（2）iteration：1个iteration等于使用batchsize个样本训练一次；
（3）epoch：1个epoch等于使用训练集中的全部样本训练一次，通俗的讲epoch的值就是整个数据集被轮几次。

	比如训练集有500个样本，batchsize = 10 ，那么训练完整个样本集：iteration=50，epoch=1.
batch: 深度学习每一次参数的更新所需要损失函数并不是由一个数据获得的，而是由一组数据加权得到的，这一组数据的数量就是batchsize。
batchsize最大是样本总数N，此时就是Full batch learning；最小是1，即每次只训练一个样本，这就是在线学习（Online Learning）。
当我们分批学习时，每次使用过全部训练数据完成一次Forword运算以及一次BP运算，成为完成了一次epoch。

```

