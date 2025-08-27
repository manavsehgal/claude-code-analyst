AWS re:Invent 2024 - Train large models on Amazon SageMaker for scale and performance (AIM308)
Dec 6, 2024 

https://www.youtube.com/watch?v=cryA1LFwS98

- Welcome everyone. Thank you for coming to our session on how to train large models on Amazon SageMaker.
I'm Rekha Seshadrinathan. I'm a Senior Manager of Product here at AWS
and I'm joined today on stage by my colleague Rama Thamman, who's also a Senior Manager on SageMaker.
The two of us are very happy to be joined by Saad Godil, CTO of Hippocratic AI, today.
Saad and his team are using SageMaker to accelerate their model training
and he's gonna share how they're doing that. - I'll let you do it, come.
- So just a couple weeks ago, a bomb cyclone ravaged through the Puget Sound area.
The storm brought with it hurricane force winds that caused unprecedented damage to power lines,
caused trees all over the city to fall down, and damaged roadways.
The storm eventually left half a million households without power for several days.
As many of us in the area tried to navigate through daily life without power,
figure out how to talk to friends and family without cell phones, how to work without internet,
how to take care of basic needs like hot water, and how to get around without being able to charge our cars,
I got to thinking, thinking about technologies that have fundamentally changed how we live our lives
and do our work, whether it was the PC
that introduced the power of mainframe computers into every household
and introduced technologies like spreadsheets and document processing,
or the internet, originally invented for military communication
but gave rise to things like e-commerce and video streaming,
or the mobile phone, that put a computer, a GPS, and a camera
into every person's hands. Do any of you remember the time when we used to actually print out directions from MapQuest
and take them along? That used to be a thing.
Well, we are very fortunate, fortunate to be living at another historic time
when there's yet another tectonic shift in the technology industry.
Generative AI has taken the world by storm and consumers everywhere have adopted it at a rapid clip.
Now here at AWS, we strongly believe that while there's a lot of excitement
about how consumers are adopting this technology, it will fundamentally change how organizations innovate
for their customers and employees. In fact, Goldman Sachs predicts,
a $7 trillion increase in GDP in the next decade
through this technology. Now, at its core, generative AI is leveraging
the latest innovations in machine learning and AI.
With the advent of the transformer architecture, foundation models or large language models came to the fore.
Now what are foundation models? They're essentially very large models
often with billions of parameters that have been trained on internet scale data.
And because of this pre-training exposure to a very large corpus of data,
these models can perform tasks in a wide variety of context.
Now, while the pre-trained models have many use cases that are exciting, the organizations that we speak to
are also very excited by the ability to train such models on their data,
which can be differentiating for their industries.
Now, here at AWS, we have always worked backwards from customers,
and about five years ago when more and more customers started doing deep learning,
we launched SageMaker Training Jobs. SageMaker Training Jobs provides a fully managed API
for customers who want to train machine learning models without managing any infrastructure.
Now, how this works is that you can simply provide us
with the kind of instances you want, the number of instances and a training script.
SageMaker will take care of spinning up the cluster, downloading the required container onto the cluster,
running your training script, and once the model is trained, we'll copy over the model artifacts
to an output location of your choice. Once the model is trained,
we automatically spin down that infrastructure and you only pay for what you used.
SageMaker training jobs is also integrated with experiment management tools,
and it comes with warm pools for low latency, and is integrated with EC2 Spot Instances.
Because of the ease of use that Training Jobs provides, it continues to be a very popular choice for our customers
who are training models and don't wanna manage any infrastructure.
But as we talked to more and more customers who were training large models for long periods of time,
a new set of challenges started to emerge in the last couple years.
The first one that we hear often from customers is about hardware.
Now, in the last few years, there've been a lot of innovations in the hardware market with gen AI.
There are new chips coming out every few months that are allowing you to train models faster and faster.
However, getting access to this latest hardware remains a challenge.
And, once you get access to this hardware, you also have to configure your clusters
and all of the software to be compatible with it.
And as the size of the models and the data sets that they're trained on
gets larger and larger, we're also seeing that the compute needs for training models
is continuously growing. In fact, it has grown over 4x every year
in the last five years, which means that customers are needing
to scale up these clusters further and further. And as the size of the clusters grow,
so does the probability of infrastructure failures. In fact, in Meta's most recent paper
on their LLaMA training, they mentioned that they faced one GPU failure
up to every three hours, which is a lot of time that your data scientists are spending
on debugging these infrastructure failures. And finally, as these compute needs grow,
you wanna make sure that your organizations are keeping their costs down and utilizing this infrastructure
as effectively as possible.
So to solve these challenges that we were hearing about, right here at re:Invent last year,
Amazon SageMaker introduced HyperPod. SageMaker HyperPod is purpose-built infrastructure
for gen AI development that can reduce your time to train models by up to 40%,
allowing you to scale across thousands of accelerators.
How do we do that? So first, SageMaker HyperPod
provides you with a resilient environment. What I mean by that is that the HyperPod clusters
come with cluster monitoring software that are monitoring the infrastructure for failures
and self-healing the nodes when a failure is detected, which reduces your time to train.
HyperPod also comes with SageMaker's distributed training libraries, which allow you to easily shard your model
and data across the cluster, making it faster to train on AWS infrastructure.
And finally, many of the customers who are training these large models
told us that they want a lot more control over the infrastructure. They wanna be able to customize it
and install whatever tools their teams needed. HyperPod allows you to SSH into the instances
and gives you full control over the computing environment.
So here are some of the core elements of HyperPod. First, on the infrastructure side,
HyperPod leverages EC2 clusters. And essentially, you have EC2 instances
that are on the same spine or availability zone, which is important for distributed training performance,
that are connected via EFA or Elastic Fabric Adapter.
This is a network interface that is specifically designed for high throughput and low latency.
Again, very important for applications like HPC and distributed training
where there's a high degree of internode communication. You also have access to FSx for Lustre,
which is a high performance distributed file system.
The HyperPod compute nodes run on the Deep Learning AMI,
which comes pre-configured with NVIDIA CUDA and the latest deep learning frameworks.
In addition, the HyperPod software also includes the distributed training libraries
that are specifically optimized for AWS network topology, and the cluster health monitoring software as well.
So I'm gonna go over some of the other key features of HyperPod, and later in the presentation,
Rama's actually going to do a demo and show you how most of these things work.
So first, in order to help customers easily create and manage these clusters,
SageMaker HyperPod provides APIs through which you can create the cluster,
update, as well as delete nodes. We're also fully integrated with the AWS console,
so you can both create your cluster as well as access and monitor your HyperPod clusters
through the UI. You can also do this through the CLI and cloud formation templates as well.
In terms of resiliency, like I mentioned, HyperPod comes with cluster health monitoring software
that is constantly monitoring the cluster for hardware failures. And when we detect a hardware failure,
we will either reboot the node or in cases when that can't be done,
we will replace that node from an AWS maintained spare pool of instances,
which comes at no cost to you. And if you submit your jobs indicating that you want your training job to auto resume
after a hardware failure, we'll also restart your training job and reload from the last saved checkpoint.
So it's completely hands-off for your data scientists and machine learning engineers.
And finally, to help you optimize cost and performance, we've also integrated
with Amazon Managed Grafana and Prometheus, so you can export your hardware metrics
into a Grafana or Prometheus workspace and monitor your cluster utilization
and make sure that you're using it as effectively as possible.
Now, an important consideration for many organizations
when they're considering their partners for gen AI is how quickly do these organizations move,
because we see that in this industry there's a new innovation coming out every few months.
Since launch of HyperPod last year, we've been continuously making updates.
And one major update that I wanna share is that just a couple months ago,
we launched Amazon EKS Support for SageMaker HyperPod.
So when we launched last year, you could orchestrate your workloads using Slurm. Well now, you can also orchestrate your workloads using EKS.
So you can either create a brand new cluster or attach HyperPod managed compute nodes
to an existing EKS control plane.
We've also updated the resiliency for HyperPod, now. So when you create your clusters,
you can optionally run deep health checks. These are NCCL tests as well as DCGM diagnostics
that you can run at the start and that will reduce the probability of failures
once you start your training. And finally, for EKS customers,
we've also enhanced the scientist experience. So, you now can submit jobs using a HyperPod CLI,
and we have Container Insights integration for utilization as well.
With the launch of EKS, we're also seeing more and more customers use their HyperPod clusters
for both training as well as inference. So if you're already using EKS to orchestrate your workloads,
you can now use the same nodes both for model development and deployment,
which can further optimize the utilization of your clusters.
So with this intro to HyperPod, I wanna hand it over to Rama who's going to do a more technical deep dive
and give you a demo of how all of this works.
- Thank you, Rekha. In the next 20 minutes or so, I will walk you through some of the technical details
and also show you a demo of HyperPod. By show of hands, how many of you are training large language models
or consider training large language models down the line? Okay, that's quite a few.
Alright, so let's start with training performance. Let's see how customers gets training performance
using HyperPod. HyperPod is specialized for training large language models
and also foundation models. When training such models, you need to have specialized parallel,
model parallel training techniques. For example, let me give you a scenario here.
Let's say you're training a 8 billion parameter model. You will need about 160 GPU memory.
If you look at just hardware from NVIDIA, H100 has 80 GB per GPU, H200 has 140 GB.
Now, for training 8 billion parameter model, you will need multiple nodes. That's where you would need all of these techniques
and HyperPod comes out-of-the-box with that. More importantly, what's important is the entire stack
will have to be optimized to use your hardware and resources in an efficient way.
Network bandwidth is super important. If you're training with tens of hundreds of nodes,
these nodes are talking to one another very frequently. After every batch, you exchange the nodes,
these are the gradients... Exchange the weights, these are the gradients. And if you have network bottleneck,
then you cannot move faster. So you need to have a high bandwidth network. With EFA, you get 400 GBPS of network bandwidth.
EFA doesn't... It bypasses the OS, it doesn't use TCP IP,
it uses something called Libfabric. And, EFA also uses NVIDIA's GPUDirect.
It can do a remote direct memory access. The network card can access memory of another GPU.
So that's how we get this high throughput. Then with Libfabric, you get support for multiple message processing interface
and also NVIDIA's common collective library.
Storage is super important. If you're training a large language model, chances are you are using lots of data,
and your training algorithm should be able to read this data faster. And to do that,
you need to have a high performance file system where you have sub-millisecond latencies
to read the data quickly. If you have to download the data onto your instance,
then train, thus your GPUs are setting idle. You don't want to have that. So you should be able to read data quickly.
And with FSx, you could concurrently access thousands of instances and hundreds of thousands of cores.
With all of these three things, customers are able to train faster. If they're able to train faster
with less bottleneck and so forth, you could reduce the overall training cost and that's how our customers are able to train
up to 40% faster using HyperPod.
Let's talk about resiliency, this is very, very important. Before you start your cluster, you should make sure your hardware is healthy.
You don't want any hardware failures because that'll slow you down further. To that end, with HyperPod,
what we do is before we hand out an instance to the cluster, we make sure we run some deep health checks.
We use NVIDIA's data center GPU management tools to run diagnostics. We pressure test the GPUs to make sure those are healthy.
We also look at CPU health, this is important. Especially when you're doing data loading,
you should be able to use hundred percent of your CPU utilization and also have the I/O operations in good standing.
We do that before the instances are given out. Once your instances are in the cluster,
we continuously monitor the GPUs. We use the same data center management tools
and we monitor for certain thresholds, looking for certain errors, looking for threshold breaches for power
and clock management and so forth, even temperature to some extent. So these are called policies and these policies are set
and those are run continuously behind the scenes. We also use NVIDIA SMI to check the health of GPUs
constantly and notify you.
And network health check is also important. The health checker also checks for connectivity
between the cards, between the instances, to make sure these instances can operate efficiently.
Now, let's look at the resiliency feature that Rekha talked about. You know, you are bound to run into error,
so you should be able to self heal. With HyperPod, let's say when you start running training,
you're constantly doing checkpoints. Large language model training usually runs weeks together,
months together. You should be able to recover from errors automatically. So with the HyperPod, what happens is,
as you're training, if one node fails, HyperPod automatically detects the error
and it'll take the node out of the cluster. It brings back a new node, does the deep health checks,
and it'll also pull down the necessary containers, then also the last checkpoint
and it starts training automatically. You see, we take the undifferentiated heavy lifting
and you don't have to worry about this. All of these things are done automatically behind the scenes.
There are times where you may want to on-demand replace a node. Sometimes the instance may go into a state
where they don't respond, so in those cases you could on-demand replace a node. If you're using Slurm, you could run that command.
If you're using EKS, you could use node labels to change the label and automatically that node will get replaced.
Ease of use is super important. Given that there's so many open source tools, so many different options for you,
we want to give you the flexibility to pick and choose the tools that you want to use.
From an orchestration standpoint, we have Managed EKS and Managed Slurm that comes as part of HyperPod.
If you want to deploy your own orchestration layer, let's say, your own Managed Kubernetes,
you can do that as well. From a job submission standpoint, you could use Ray, Run:ai, Kubectl, whatever is your choice.
For observability, we have support for Prometheus, Grafana, CloudWatch.
And in some cases you may want to connect to the cluster from a notebook or from your laptop.
So from that, you can use SageMaker Studio or even use Jupyter Notebooks to connect to the cluster
and submit training jobs and so forth. For training libraries, HyperPod comes
with some of these popular training frameworks like PyTorch and so forth, with all the versioning and stuff
so that you don't have to worry about those. I talked about training strategies, we pack in all of the popular ones there.
And with experimentation, we do have support for tools such as Kubeflow, Weights and Biases, MLflow and so forth.
So you could readily use it out-of-the-box. We also provide first party containers like machine images,
Deep Learning Containers and so forth, so you could easily pull down and start working on it.
Device drivers, toolkits, all comes part of it. Hardware is super important.
With HyperPod, you get the latest and greatest GPUs. From NVIDIA, we have H200 which is P5e, H100 is P5,
and also our own silicon, that's the Trainium instances that are available as part of HyperPod.
I touched on storage and networking. Now, let's go through the demo.
Before I show you the demo, I'll set you the... I'll go through the steps that I'm gonna show you.
First is preparation step where you need to have certain resources ready before you can start the cluster,
like your networking setup and so forth. Then I'll show you how to create a HyperPod cluster.
As part of it, you can create a lifecycle script. So this script is used to set up certain things.
If you want to install certain things in the nodes, you can do that, that's an optional step.
Then I'll show you how to create a cluster config. Here, you will set up the head node, the compute nodes.
I'll also show you how to create different groups like an inference group and another one for training and so forth.
Then lastly, I'll show you how to create a cluster. So up until this point, it's all admin set-up,
mostly admins do it as a one-time step and so forth. And once you have the cluster,
that's when your data scientists would come in. I'll show you how to run a training job,
connect to a node to run diagnostic commands. Then, show you resiliency features.
Here, I'll show you when I inject error into one of the nodes, I'll show you how HyperPod
automatically replaces the node for you. Then lastly, observability. This is super important
because you need to be able to monitor different metrics on your cluster, like temperature, GPU utilization,
and so forth. So we have a rich set of capabilities there. And for the demo, I'm gonna use this workshop.
I'll make this link available in the end of this presentation, but with this you can easily set up your Kubernetes...
Easily set up your HyperPod cluster, then test out and use the same config for your production.
Alright, let's go through the demo real quick here.
So here's the HyperPod workshop I talked about. Yeah, you can test out different features here.
I'm gonna start with the prerequisite here. So here, we are setting up some of the basic resources that you need.
There are a couple of options for you. You could either do the full deployment where we would set up everything for you
from networking and all of those things, or you could do integrative or minimal deployment setup
where you could use your existing resources like networking and so forth.
And for this one, I'm gonna use full deployment mode. When I click on that, the cloud formation template
is gonna set up all the resources that I need. You could go and change your availability zone,
other details like the (indistinct) and so forth. And once you create the stack,
behind the scenes we will create all the resources. You can see the EKS cluster is being created.
Other networking resources that you need will get created automatically like your VPC,
your subnet and so forth. This may take about couple of minutes, but once that's done, you have all the resources
that are necessary for you to create a cluster. As part of creating a cluster, I'll show you how to create a lifecycle config.
This is to set up whatever installations that you need or configurations that you want to make as part of the cluster.
The steps are very simple, create a script, put all the commands that you need
and you can save this file on the S3 location.
Just copy it over and we will reference this location when we create the cluster.
That's how simple it is for the lifecycle config. Now for cluster creation, there are a couple of options.
Either you could use the CLI to create the cluster or you could use the HyperPod console to create the cluster.
For this demo, I'm gonna to show you how to use the HyperPod console to create the cluster.
So here's the SageMaker console. You can navigate to the HyperPod console,
it's on the left there. And once you go into cluster management, you will see the EKS cluster we just added here.
I'm gonna select that cluster and now I can give a name for the cluster,
I'll say demo cluster. And I can create different instance groups.
One group for inference, one group for training. I can have heterogeneous clusters, different instance types and so forth.
Here, I'm gonna use G5 instance, I'm gonna have just one group.
I'm gonna have about eight instances. I'm gonna specify the location of my lifecycle script
where it was, and I also will enable some of the resiliency checks
that I talked about, the deep health checks. And I can do... I can use the advanced configuration
to set up storage and other details that you may need.
And here you can select the network that we created as part of resources.
Then finally, when you hit submit here, behind the scenes the cluster will get created.
It may take 10 to 15 minutes depending upon the number of instances that you have in the cluster.
And here you will see, initially, the instances will come up as pending state.
Then we'll do the deep health checks for you to make sure the hardware is in good standing. Then, the instances will go into a running state,
shortly here. Now the cluster is ready and your data scientists can come and submit jobs
and run training. I'll show you how to do, how to submit a training job.
The workshop has different examples. Here, I'm gonna use PyTorch, a fully sharded example here.
You can also alter this to change however you want, but here I'm gonna use the training example assets.
Using kubectl, I'm gonna to submit the job. You can see, you could use the apply command.
And behind the scenes, the job is being submitted and you will see there are eight workers.
I can go look at which one is the leader node here by looking at the logs.
And you can see the training has begun, the loss minimization is going on here.
So that's how simple it is. You submit the job and the training starts. And in some cases,
you may want to go into each of these nodes to figure out how your GPU is being utilized.
So that's very straightforward. All you need to know is the node name that you want to get into,
then you can use AWS's session manager to connect to that instance.
So you start the session and once you're on, it's like any other EC2 instance.
You could log in as another user, run commands that you need,
like top command to look at all the processes. Also you can run NVIDIA SMI to look at your GPU utilization
and GPU health as well.
So that's how easy it is to get onto an instance. Now let's look at the resiliency feature here.
With the resiliency, there are two scenarios here. One, HyperPod automatically replacing a node
when there's an error. The second scenario is on-demand if you want to replace a node, you can do that.
But for this demo I'm gonna show you how HyperPod automatically replaces the node for you.
So here, I will have the setup of...
So you can see, I have the workers on one side and also the nodes on the other side. I have eight different nodes.
What I'm gonna do is I'm going to log into the third node there. I will do a SSM session there
and I'm gonna inject error into the logs. So I write some error messages into the log.
Then, the HyperPod automatically picks up that particular node. You can see, the third node will go into a not-ready state.
And you'll also see that the worker will go into a pending state and HyperPod will take that node out of that cluster.
Then, it'll bring in a new node, it'll do the deep health checks and so forth.
And here you can see, it added a new node for you. The third one from the bottom.
And once the node is added, it'll go through all the setup like the downloading the container and so forth.
And then, once that's done, it'll also bring down the checkpoint to start the training where it left off.
Then, you can log into that particular node to see how the training is going. You can see that's a lot of undifferentiated heavy lifting,
it's automatically done by HyperPod. You don't have to worry about it.
Now, let's look at observability, this is super important. When there are lot of nodes,
you need to be able to monitor for temperature, monitor for GPU utilization, CPU utilization and so forth.
Especially when you're training, you may not get the best utilization so you have to go iteratively
and you have to be able to monitor all of these things. So in the HyperPod console,
you can click on Container Insights there and that'll take you to the observability page.
And you can monitor metrics at the cluster level, you can see I have eight nodes, the CPU utilization,
I have high GPU utilization. That's what you want to see when you are finally done.
You can see there are a lot of other metrics like amount of data that's going in and out to see how your network is being utilized.
You can also monitor the temperature that I talked about.
GPU temperature is super important to watch for and a number of other metrics that you could leverage
and set alerts and so forth. You can also look at pod-level metrics.
So you can see there are about 95 containers running. You can monitor at a granular level.
Let's look at GPU utilization here for one of the nodes.
You can see there are eight workers and you could drill down to one of the workers that you want to see, how GPU is being utilized.
So you can see the rich set of features that are available for you.
So, so far what you've seen is how to set up a cluster quickly, how to submit a job, then how to monitor,
and also showed you the resiliency feature. With that, now let me invite Saad Godil
to talk about their journey of using HyperPod. Saad, take it away.
- Alright, thanks, Rama. Hi, everyone, I'm Saad Godil.
I'm the co-founder and CTO of Hippocratic AI.
Hold on, let me see. Let me go to my slides real quick. So, let me tell you a little bit about Hippocratic AI
and what we're doing. So we are tackling the worldwide nurse shortage by building gen AI based autopilot agents
that can basically do clinical tasks. And what we're specifically doing here is patient outbound.
So we'll call patients on the phone and be able to autonomously reach out and perform a task
using our technology. Now, when we talk about gen AI, there's many different ways
that you can use the technology, right? And I think what you'll find is that a lot of gen AI companies in healthcare
are building what we call copilot solutions, right? So a good example of this is you'll see these EMR summarization,
there's ambient listening. A lot of these products are basically targeted at helping a human in the loop become more efficient.
The downside of this is, you know, you're basically not able to get a lot of upside, right?
You could at max, you know, may improve someone's productivity by 10% or 15%, but that's not gonna solve the nurse shortage
that I was talking about. You know, we need something much, much bigger leverage. And this is where the autopilot agents come in, right?
These autonomous agents can actually fully do a task and will allow much, much larger scaling.
And so, what are some of the things that we do? So one example is like a pre-op call. So, you know, you have a colonoscopy appointment coming up,
we'll call you three days before your appointment, you know, make sure you start taking your bowel prep solution, make sure you start your low fiber diet.
We'll call you one day before the appointment and say, "Hey, now you gotta stop eating solid foods." Make sure you start your clear liquid diet
and then, you know, six hours before your appointment, make sure you stop drinking water as well. So, you know, we can do all these,
what I call care plan instructions and just communicate that with the patients and help them adhere to it. Another example is post-op call.
You just get discharged from a procedure, we'll call you up after the procedure, say, "Hey, have you had a chance to pick up your medications?
Were there any complications? Did you have any questions about the care plan the doctor gave you that I can answer for you?" And another big use case
that we're seeing a lot of interest in is doing health risk assessments and annual wellness visit intake forms,
where basically we can very efficient- information from the patients at their convenience
and basically, which is something that we think gen AI can fully automate and do efficiently.
But, you know, the most exciting aspect of this is really, you know, what we think this will lead to, right?
So, right now we're talking about tasks that we can augment and do ourselves, but we actually think as the cost of these calls goes to zero,
we think it's gonna unlock a whole plethora of use cases and care management that is not even done today,
that we can't even think of, right? And so, this is actually what I think is the most exciting, compelling use of gen AI. So a great example of this is, you know,
we had one of our customers come up to us and say, "Could we do a heat risk assessment?" So heat waves are coming in,
they can identify which of their patient population, subset of their patient population is most at risk
and we can just call all of them up instantly, right? This is the power of gen AI, you can instantly scale it up as needed,
call 'em up every day, do a health risk assessment, make sure if they're at risk of suffering from a heat stroke
and we'll just basically, you know, transport them to a cooling center, right? You can't do this with humans. You can't get enough people online at once,
make all the calls, this is a perfect use of gen AI. And so, there's stuff like this that I think we'll be able to do that we just were not able to do
before this was available. Now, one of the most important features
that we have in our system is safety, as you can imagine. And the way that we do safety is we introduce this concept
called constellation architecture. Turns out, you can't do it with just one model. So our constellation architecture
consists of 20 different models or over 20 models, and we have a whole bunch of specialist models
that work with the primary model to deliver the safe experience that we need. So we'll have, you know, a model that's just focused on over-the-counter,
you know, disallowed over-the-counter medications. There's a model that's just looking at your medications and making sure you're adhering
to your prescriptions as required. There's a model that can do your lab analysis and give you the appropriate advice.
So, you know, these specialist models allow us to train and specialize these models for these, what I call safety verticals, safety axes.
And for each of these safety axes, we can build a model that can deliver the level of safety that is required.
Now what we do is we train these models based on open-source models. So we'll take the open-source models and then of course, we'll train them
with our, you know, custom proprietary data sets. But the specialization is what allowed us
to get that last bit of performance to give the, you know, to provide the safety that we need to provide. Now, very recently,
we actually upgraded our constellation architecture. So, you know, first one was Polaris 1.0, we went to Polaris 2.0, and our largest model
basically went from 70 billion parameters to 405 billion parameters.
And, you know, that's a 6x increase in the number of parameters. And as you can imagine, we're a real time application, right?
We're calling patients on the phone, so latency matters a lot. And, one of the big challenges that we had is when we upgraded these models, which actually was great
because the reasoning capabilities that we got from the upgrade was significant, but it posed a real big challenge on inference
and how do we maintain our low latency? And you'll see the plot on the right, you know, this is a box and whiskers plot of our latency distribution.
We actually were able to, through a bunch of very innovative, clever techniques, we were actually able to keep the latency the same.
And so some of those techniques that we did, you know, we did calibrated FP8 quantization. Usually, when you quantize,
you are trading off some kind of performance. But with calibrating it to our trainings, that we were able to actually basically not lose
any of our clinical safety aspects that we cared about. We also did a lot of aggressive prefix caching.
This is actually the key breakthrough. It turns out, when you're having a long conversation,
you know, your input prompt is very large and that can take a long time to go process, especially for a large model.
But, the only thing that's changing from one call to the next is literally just the,
you know, the one patient turn that's been added. And so what you can do is you can leverage the pre-fill from the previous query.
And then, this is how you can actually save a bunch of time and lower the latency. And so aggressive prefix caching was critical.
Then, of course, you know, we're scaling up to, you know, many, many calls and parallels, so if we have multiple nodes.
And so if you're gonna do any kind of caching, we also have to do some kind of routing to make sure that, you know, calls from the same conversation
go to the same model. So we had some conversation based routing as well that we had to add.
Now, all of these models that I talked about were trained on SageMaker HyperPod. And, you know, one of the things about our use case is...
You know, because we're HIPAA compliant, and you know, patient data is really important,
we actually have a number of different clusters. So all of our production inference workloads that has patient sensitive patient information
is actually run on a completely different account, on a completely different cluster. And our training and all of the dev work that we do
is done on a separate account. And so, we basically use many, many different accounts for different environments to ensure that we have the right kind of data separation
and security and privileges. And so this is kind of what our training cluster looks like.
I think Rama and you know, showed you a bunch of examples. As you'll see, we're using a lot of the services that he talked about, right?
So we're using FSx and S3 for our storage to get fast storage into the GPUs to train our models.
You know, we're using Grafana and Prometheus for logging and metrics. And as you can tell, you know, these GPUs are fairly expensive
and you know, we need to do extensive monitoring to make sure that our utilizations are good. And so we utilize all these metrics
to ensure that we hit our utilization targets. Now moving on to inference architecture,
it looks pretty much the same. You'll see that we don't have a lot of the user accesses because we don't actually give a lot of users
access to our production clusters, it's very restricted. And the one addition that we have is, you'll see on the top we have an application load balancer.
And this actually... We actually use Kong as our API gateway manager because that's how our models will communicate
to the application layer is through the API. Now, I think, a bunch of features
I think Rama covered in his presentation, which we're definitely using. So first off, right, he showed you how easy it is
to kind of spin up a cluster and spin it down. We love that, right, because we're... Like I said, we have many, many different clusters and being able to completely automate the spin-up
and tear-down of a cluster is super critical. So we have Terraform scripts that will just go bring it up and bring it down as needed.
Because we have multiple clusters, we're often, you know, balancing the needs between inference and training,
between different kind of workloads that we have. And so being able to move these GPUs from one cluster
to another is extremely important for us to be able to optimize and, you know, optimally use this limited resource that we have.
And then of course, when we do that and we bring it up in another cluster, it's really great that, you know, HyperPod has these lifecycle scripts
that will just set up the configuration of the node and we don't have to do anything, we just bring it up and it's set up and configured correctly right from the get go.
And then of course, you know, with GPUs, reliability is really critical, right? You will have faulty nodes
and you know, being able to leverage, you know, the HyperPod feature where we can just swap out a faulty node with a backup reserved instance,
it gets us up and running right away without wasting any time, which is a super, super cool feature.
In terms of looking ahead, you know, things that we are really thinking about, what's on our mind now is Elastic GPU compute.
You know, when we're doing these kind of calls to our patients, you know, it turns out there's really only six hours in the day
where patients wanna be called. And so, you know, we're now working with AWS to figure out how can we actually get access
to burst peak GPU compute, so we can actually scale up our inferencing workloads
and, you know, hit all of our business goals. The other big feature, you know, I'm really excited about EKS on SageMaker HyperPod, right?
As you can imagine, our inference is scaling up pretty significantly. We need to do auto-scaling both up and down
to manage the complex workloads that we have. And so we need to basically automate all of our orchestration and all the scaling up that I talked about.
And so we think building it on Kubernetes with EKS is the right strategy and so we're gonna be investing in that
and building that up next. Okay, and I'll kind of leave you guys with this idea, right?
So, from the beginning of time, healthcare has always been constrained
by the healthcare professionals, right? The whole system has been designed with that kind of constraint in mind. And for the first time, with gen AI,
we now can truly have abundance in healthcare and that's really what gen AI is gonna help us accomplish.
And we're happy to partner with HyperPod and the SageMaker team to help us go deliver on this vision.
Alright, thank you. (audience applauding)
- Thank you. Yeah, before we wrap up, I wanted to leave you with some key takeaways.
First, with SageMaker HyperPod, you can reduce time to train by up to 40%.
With the resiliency features and distributed training libraries that we offer,
you can scale to thousands of accelerators easily using the APIs and console UI that we provide.
You can optimize for cost and scale with the monitoring infrastructure that we provide,
so you can look at utilization of your GPUs and CPUs. And finally, we are flexible.
HyperPod is flexible and customizable, so you can SSH into the instances and customize the stack how you wish.
Since launch, companies of all sizes and from all industries
are leveraging SageMaker to accelerate their gen AI development.
These include top startups like Hugging Face, Perplexity AI, and Hippocratic AI,
and enterprises like Salesforce and Thomson Reuters.
And many of them are saying that HyperPod is saving them
hundreds of hours in training time and improving their data science productivity.
For those of you wanting to get started on HyperPod, here are some resources, feel free to take pictures.
And many of these customers are also in a customer panel, which is happening at 2:30 today.
So if you wanna hear more from Hopper AI, Hugging Face or Writer AI,
there's a session at 2:30, AIM229, that I encourage you to attend as well.
Yeah, so thank you for attending and listening and we'll be here to take more questions. (audience applauding)