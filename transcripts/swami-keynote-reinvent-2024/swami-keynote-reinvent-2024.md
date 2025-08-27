AWS re:Invent 2024 - Keynote with Dr. Swami Sivasubramanian
Dec 4, 2024 

https://www.youtube.com/watch?v=qGzYTg5FIA4

Please welcome Vice President of AI and Data at AWS,
Dr. Swami Sivasubramanian. [music and applause]
All right. Good morning, everyone. Thank you for joining us today at re:Invent 2024.
It's been another monumental year, one where every organization across every industry
is challenging the status quo. Disruption is the new normal, and rapid innovation is now table stakes.
If you look back at the history, as creators, tinkerers and technologists, we always have an innate desire to push beyond our natural limits.
Building upon the achievements of the previous inventors, until one day when we experience this magical moment
where every incremental achievement suddenly culminates into something larger than the sum of its parts,
then everything takes off. Let's look back to a defining breakthrough
in the aviation history – the Wright brothers’ first flight in 1903.
This 12 second flight didn't happen in isolation. It represented centuries of technological advancement,
right from da Vinci’s sketches that laid the conceptual groundwork for human flight
and the early designs of the fixed-wing aircraft that separated the concept of lift and propulsion.
And of course, the first steam powered aircraft that showcased the potential of powered flight,
and a series of glider experiments which provided crucial data on lift
and drag that directly inspired the Wright brothers. If you look back, the convergence of all of these achievements,
plus innovations in material sciences, manufacturing and combustion engines,
ultimately made powered flight possible. So while the Wright brothers can't take all the credit
for their 12 seconds of success, they became the integrators for every dreamer
that built upon the work of those before them. Today, we stand at a similar point of convergence with generative AI.
This new era of AI innovation brings together decades of research and scientific advancement.
From the first artificial neural network, the perceptron model, to back propagation,
which enabled efficient training for multi-layered models
and of course, to uncovering the massive potential of unsupervised pre-training, which gave us the ability to learn from data
that need not be annotated for every bit. And of course, the transformer architectures
that revolutionized natural language processing. However, all these discoveries alone were not enough.
The convergence of massive data sets and specialized compute, all made available via the cloud,
created the perfect conditions for AI to flourish. And now we have reached yet another tipping point with generative AI.
New tools and user interfaces are enabling widespread adoption
at an unprecedented pace, driving efficiency and unlocking creativity for all of us.
If you look, customer service representatives are using AI to draft personalized customer responses in just seconds.
Marketers are generating compelling ad copies and images at scale,
and developers are leveraging GenAI assistance to remove the heavy lifting
from end-to-end software development process. As we reflect on the convergence that made GenAI possible,
I can't help but look back at my 18-year journey at Amazon and the inception of AWS.
I didn't always know that our experiments would lead. I was driven by a relentless curiosity
and an innate desire to solve real customer problems. Each innovation we delivered on our journey,
right from scalable infrastructure with S3, to database breakthroughs with DynamoDB
and scalable analytics with EMR and Redshift. And of course, to the democratization of machine learning,
with SageMaker and Bedrock; built upon the last,
unlocking incremental values for customers as their use cases evolved over time.
Like Intuit, which leverages S3 to build their data lakes on AWS,
they use Amazon Athena EMR and Glue to run analytics and Amazon SageMaker as a core element for their ML strategy.
And GE Healthcare, who are using the power of S3, Redshift, and SageMaker to run analytics and ML workflows
for all their medical use cases. The breadth and depth of these services
has been critical for our customers as they scale their data and ML related projects.
But as more and more of our customers want to leverage these similar data sets across multiple use cases.
They didn't want to jump between multiple services to get their job done. We saw an enormous opportunity to harness
the convergence of big data, analytics, machine learning, and now GenAI to create a new and unified experience
that would accelerate their workflows and enhance collaboration. That's why yesterday, Matt shared how the next generation of SageMaker
is now the center for all your data, analytics and AI. It brings together our key learnings across big data,
fast SQL analytics, machine learning model development, and GenAI into one single unified platform.
It's more than just integrating a bunch of tools. It represents years of work, countless customer conversations,
and the collective expertise of teams across AWS. We are thrilled to bring you this new experience,
but, it does not mean we are slowing down on enhancing the capabilities, especially the training capabilities of SageMaker
that you all already know and love today, which is now called SageMaker AI.
SageMaker AI represents another convergence of innovations in the world of data and ML.
It is built on decades of neural network research to make deep learning more accessible and scalable for the first time.
It's the culmination of breakthroughs in compute power, ML, distributed systems, and user experience design.
SageMaker AI provides you the tools and workflows that remove the heavy lifting
from machine learning and analytics life cycle. Right from data prep to authoring ML models,
to doing the training to ML deployment, to observability, all these things, and it provides you all the tools
and brings them together in one place. That's why hundreds of thousands of customers
are using SageMaker AI to train and deploy their foundation models with their data.
Since last year, we have released more than 140 new capabilities
to help customers build their models faster and more efficiently.
However, with the advent of GenAI, we knew you needed new tools
and capabilities to support training and inference for all these models. These very large models with billions or tens of billions,
if not hundreds of billions of parameters. That's because building and training
these large foundation models is complex and requires deep machine learning expertise.
First, you had to collect large amounts of data. Then you create a large cluster of these machine
learning accelerators. Then you distribute your model training across these clusters.
Then, while during this multiple-week process you frequently stop and inspect if the model is converging.
If not, actually make the appropriate corrections. And in the middle of this long process,
if a hardware accelerator fails, then you've got to manually remediate all these issues.
To help all the heavy lifting associated with this training process, last year we launched SageMaker HyperPod.
HyperPod comes with advanced resilience capabilities that ensures that your cluster can automatically recover
from failures across the full stack. It has fast check-pointing and active compute resource management.
HyperPod has become the chosen infrastructure for our customers to train their foundation models.
In fact, leading startups like Writer AI and Perplexity, and large enterprises like Thomson Reuters and Salesforce
are accelerating their model development with HyperPod. However, as the space moves so fast
and scale is growing at an unprecedented pace, we are currently facing a critical inflection point
when it comes to model training. As these models are becoming increasingly sophisticated,
we are facing unprecedented challenges with compute resources, energy consumption and data quality.
The current paradigm of training massive models with billions and soon, trillions of parameters, is pushing us to explore
more efficient architectures and ways to train.
Traditional scaling techniques are approaching their physical and economic limitations
that demand a fundamental rethinking of our methods. As Peter mentioned on Monday, we are heavily investing in providing
you the best-in-class machine learning infrastructure with Trn2 and our specialized GPU instances.
But we know that you are still tackling challenges with model training and inference,
especially when it comes to securing and efficiently managing these compute resources.
Now let's look at a typical example. Imagine you need to train a large language model
using accelerators for a total of 30 days. These instances are in high demand, so you end up spending a lot of time
searching for available capacity across AZs and regions over a large time window.
Once you procure that capacity and you get, let's say, discontinuous blocks, you have to manage these
and save and restore checkpoints and move training data closer to where you get the capacity across AZs and regions.
So we wondered, wouldn't it be nice if you can define your compute requirements
and desired training time frames then have SageMaker take care of the rest?
That's why today, I'm very excited to introduce SageMaker HyperPod flexible training plans.
[applause]
This is an incredible capability when you think about it. You can quickly create a training plan
to automatically reserve a capacity and it sets up a cluster, creates model training jobs,
saving your data science teams weeks to train a model. HyperPod is built on EC2 capacity
blocks to create the optimal training plan based on your timeline and budget.
Now, if you look at the example I just showed, in this case, HyperPod will present you with the individual time slices
and AZs to accelerate model readiness. And with efficient check-pointing and resuming,
HyperPod automatically takes care of any instance interruptions and helps you continue training without any manual intervention.
In a world where a capacity situation is dynamic, this is going to be a game changer.
Now, another challenge our customers face is how to efficiently manage compute resources
across multiple teams and projects. We live in a world where compute resources are finite and expensive,
and it can be difficult to maximize utilization and efficiently allocate resources,
which is typically done through spreadsheets and calendars. Let's look at an example.
Imagine you have 1000 accelerators like TRN2. During the day they are heavily used for inference,
but at night a large portion of these costly resources are sitting idle when the inference demand might be very low.
Now, without a strategic approach to resource allocation, you are not only missing opportunities,
but you are also leaving money on the table. You might be wondering this problem is simple, I can write a script to move capacity from one project to another,
but in the real world, you can imagine the real world is lot more complex
– with multiple inference projects, multiple training projects, and fine-tuning and experimentation projects running concurrently
and all of them competing to the same compute resources. This was true for our internal teams at Amazon
as we rapidly scaled with GenAI. So to remove this heavy lifting, we developed a solution
that dynamically allocates compute resources for us. We also built real-time analytics
and insights for compute allocation and utilization. This helped us drive utilization
of accelerated compute across projects with Amazon to over 90%.
So when I shared this success story with CIOs and CEOs, they told me, they are facing this exact same problem as they scale.
And they said they wanted to take advantage of this solution on SageMaker too.
So today we are doing just that. I'm thrilled to announce SageMaker HyperPod Task Governance.
[applause] This innovation helps you maximize compute resource
utilization by automating the prioritization and management of these GenAI tasks, reducing the cost by up to 40%.
With HyperPod Task Governance, you can easily define your priorities across various model tasks,
from inference to fine-tuning to training and many others. Then, as business leaders or technology leaders,
you can set up limits for compute resources by teams or project,
and HyperPod will dynamically allocate resources to ensure that these resources are allocated to your highest priority tasks
and make sure they are completed on time. You can also monitor resource utilization
and gain real time insights into tasks, so that you can decrease the wait times
by constantly tuning your priorities and allocation.
Now, while customers are harnessing the power of SageMaker AI
to build and train their ML models, they also told us they wanted to use these specialized
third party applications that support various part of MLOps lifecycle, too.
For instance, there are popular AI partner applications so far like Comet, Deepchecks, Fiddler, and Lakera.
These apps cover a wide variety of tasks for your use cases such as tracking and managing training experiments.
They are evaluating the quality of your models or monitoring the model performance in production
and protecting your AI apps from security threats. However, you told us that while we love these partner apps on SageMaker,
putting them together with SageMaker can be time consuming. For instance, you have to find the right solution,
and then you have to manage the infrastructure for these applications. Then you had to spend time and resources
as you scale your own MLOps pipeline. And then you may also be worried that the security of your data
and you don't want it to be shared outside your VPC, across multiple third party tools.
We wanted to make it easier to combine the power of these specialized apps with the managed capability
and security of SageMaker AI. That's why today I'm pleased to announce
that now you can deploy all these partner apps in SageMaker.
[applause] These apps are going to help you accelerate
the model development lifecycle with a seamless, fully managed experience with no infrastructure to provision or manage.
And your data never leaves the security and privacy of your SageMaker development environment.
We are excited to for you to get your hands on these capabilities.
And you can imagine we will keep adding more partner apps to SageMaker AI very soon.
With all of these advancements, we have covered today in SageMaker, we are fundamentally reimagining the way
you will build and scale foundation models by maximizing training efficiency and lowering costs.
Next, I would like to invite Raji Arasu, EVP and CTO for Autodesk to share how they are leveraging SageMaker
to revolutionize 3D design. [music playing]
We’re the people who do this.
We’re the people who do this. [music playing]
[applause] Iconic structures, groundbreaking products
and memorable entertainment. Many of the amazing things you and I experience every day
are created with Autodesk software. Autodesk has been a pioneer in design and make for over 40 years.
Today, our customers, like yours, are facing unprecedented demand and disruption.
Architects and contractors are under immense pressure to construct infrastructure and buildings
that are timely, affordable and sustainable. Manufacturers are being challenged
to rapidly bring new products to market, while grappling with significant supply chain
delays and labor shortages, and production studios of all sizes are struggling to keep up
with consumers demand and constant demand for fresh content.
Like many of you, this is what gets me fired up. It's the opportunity to solve the multi-dimensional problems
that innovators and creatives face today. Go faster, cut costs, fewer resources,
and don't forget ensures sustainability at every step.
So to help our customers get ahead of these disruptive forces,
Autodesk is leading the charge on 3D generative AI
made possible by AWS. We are developing generative AI foundation models
unlike any that currently exist. So what makes our foundation models different?
First, the AI inputs for design and make
and the outputs are incredibly complex. Our billion parameter model, Project Bernini is a prime example
of overcoming these challenges. And unlike other models, it takes multimodal inputs,
text sketches, voxels, point clouds that replicate the creators design process.
Second, unlike the general purpose AI, these models are designed to generate 2D and 3D CAD geometry.
Geometry that requires spatial and structural reasoning
grounded in the laws of physics. Our foundation models distinguish between geometry and texture,
allowing our customers to create designs that are not only visually striking,
but also constructible and manufacturable with precision and accuracy.
I love this dance. I could do that forever. Autodesk is uniquely positioned
to take on the challenge with a deep expertise in connecting physical and digital worlds
for millions of projects globally. Combined with cutting edge AI research.
When we started on this ambitious journey to build foundation models, we turned to AWS,
our partner on cloud, data and AI, for the past 15 years.
Our first challenge was extracting massive amounts of intelligence from large design files,
turning it into cloud based, granular data. So imagine a single floor of an office
building that contains about 100MB of design data.
Now extend that to 30-storey skyscraper, which is three gigabytes of data.
Now let's scale that to a complex development project of office buildings and residential towers and supporting infrastructure.
By the way, that is just one project. We are working with millions of projects
resulting in billions of objects and petabytes of data of different sizes, shapes and workloads.
Using DynamoDB as the primary database, we created a canonical data model
that can handle these billions of objects, and for sure, we push DynamoDB to its limits with writes
that happen across hundreds of partitions. And partnering with AWS, we were able to scale and fine tune
it for high throughput and near zero latency.
Next up was data preparation with massive, complex historical data
we were unsure if our pipelines could handle the heavy lifting. Tasks such as characterization, featurization, and tokenization.
But by combining EMR, EKS, Glue and SageMaker, we not only scaled seamlessly,
but also delivered high quality and compliant results.
And a huge side benefit of keeping it all within the same cloud was streamline operation and boosted security posture.
The next challenge was training foundational models and doing it so quickly without breaking the bank,
which I'm sure all of you worry about. With so many GPU options out there,
SageMaker made it easy to test the various instances without the hassle of managing infrastructure and letting us
do the things we are best at, which is data prep, model development and developing customer-facing AI features.
Elastic Fabric Adapter further boosted performance, speeding our distributed array jobs
and delivering us 50% faster training times, well beyond our expectation.
Now with a final challenge was managing the complexity of inferencing large foundation models.
With SageMaker's, auto scaling and multimodal endpoints, we now seamlessly support both real time and batch inferencing,
achieving high throughput, minimal latency, and maximum cost efficiency.
Now, when I pull it all together, this machine learning environment powered by SageMaker
and the associated AI service has been a game changer for Autodesk. It reduced our foundation model deployment by half.
Increased AI productivity by 30%, while keeping operational costs steady.
By the way, this is more than internal productivity and efficiency.
We have started to roll out AI features built on these foundation models to our customers, and they're loving it.
Features that automatically generate sketch constraints and identify
and classify parts in product design. You heard what Swami said – it is more than modern development.
It is making sure we have those human interactions which are intuitive.
So these are intuitive AI features that act as a design partner for the customer,
helping them balance parameters such as material, strength, cost
so they can zone in on that one optimal design. All of this to minimize tedious tasks and maximize creativity.
I am incredibly excited about what we are building with AWS. Imagine a future where factories can instantly
with AI ship product lines with almost zero downtime.
And for the media and entertainment people in this crowd, what if production studios can swap an animated character,
populate a virtual scene in seconds? And for architects and contractors,
AI can analyze existing structures, identify problems, and suggest fixes.
Now what if Autodesk could speed up development for our AI teams by 5X?
Thanks to Amazon SageMaker Unified Studio.
Together with AWS, we are not just empowering today's creators. We are inspiring the next generation to build smarter
and more sustainable worlds. Whether they are designing the LA ‘28 Olympic and Paralympic Games,
creating solar powered smart vehicles of the future, or coral reef skeletons that is going to transform
and restore the ocean floor. We are shaping the future of our customers
so they can make anything and we are just getting started.
[music and applause]
Thank you Raji. I am amazed by all the innovation that Autodesk has accomplished over the years
that we have worked together. And I'm excited to see you pushing the boundaries of 3D CAD with GenAI.
As an engineering student in my undergrad, I never thought design was going to be completely transformed this way.
Now moving on. AWS will continue to reimagine the way you build and scale your foundation models,
but we are also helping you leverage these foundation models to build and deploy these GenAI apps through the inference process.
Inference is where these foundation models step out of the lab and into the wild to help us make decisions
that can transform industries, save lives, or simply make our daily experiences a little more magical.
However, as many of you look to run inference at scale, you will need increasingly sophisticated tools
to customize models with your data. While ML scientists have the expertise
to manage these evolving needs, many app developers who are tasked with building these GenAI apps do not have that.
That's why we built Amazon Bedrock. Bedrock is your building block for GenAI inference.
It's a fully managed service that makes it easy for app developers to build and scale GenAI apps with the access to the latest model,
innovations and tooling all in one place. We have invested in creating a seamless developer experience
with the right tools for every inference-related task, like choosing the best model, optimizing them for cost, latency,
and accuracy, customizing models with your data, applying safety and responsible AI checks,
and building and orchestrating AI agents. While we have made significant investments
in creating a seamless developer experience on Bedrock, we are continuing to tackle
even more roadblocks that GenAI developers are facing today. I'm going to dive deeper into each of these areas,
starting with selecting and optimizing the right models.
First, developers need the right models for their applications, which is why we offer a diverse set of options
that are capable of tackling virtually any task imaginable.
This includes powerful models from leading providers like Anthropic, Meta,
Mistral AI, Amazon, Stability, Cohere, and many more.
Many of you in this audience have likely experimented with some of these models,
and in an era where AI breakthroughs are virtually happening every week,
we are continuously invested in offering you access to the latest innovations.
Like in March, we first added support for Mistral AI’s high performing frontier models with open weights.
And in July, we added support for the world's largest publicly available LLM,
Meta's Llama 3.1 405B. And in September we offered
three of Stability AI’s best image generating models in Bedrock.
And just last month, we announced support for Anthropic's groundbreaking Claude 3.5 Haiku model that can perceive
and interact with computer interfaces. And finally, just yesterday,
we announced Amazon's new Nova family of models in Amazon Bedrock.
This new collection of models, including multimodal understanding models,
video and image generation models, as well as the price performant text to text models.
As Andy said, our internal teams have already put some of these models to work across Amazon,
and some of the early results are quite astounding. But in true Amazon fashion, we are not slowing down on expanding
the number of models our customers can access, including the latest models from the hottest startups.
That's why today I'm happy to share that poolside is coming to Bedrock early next year.
[cheering and applause] poolside is a really amazing startup
designed for software development workflows, and their assistant is powered by their malibu and point models.
And they excel at code generation, testing, documentation, and other kind of development tasks.
AWS is the first cloud provider to offer access to poolside’s assistant and fully managed models.
Now, in addition to models that tackle developer pain points, we are also empowering you to innovate
with the latest image generation models too. That's why today I'm excited to announce Stability AI’s
Stable Diffusion 3.5 model is coming to Bedrock as well.
This advanced text to image model, which was trained on SageMaker HyperPod,
is the most powerful, Stable Diffusion family of models. You can generate high quality images from text descriptions
to create conceptual arts to visual effects prototyping and detailed product imagery.
And finally, many of you told us you wanted access to cutting edge video generation models,
which is why we are adding even more options for your use cases. That's why today I'm thrilled to announce
that Luma AI is coming to Bedrock very soon.
Luma’s model innovation marked a significant advancement in AI-assisted video creation,
enabling you to generate high quality, realistic videos from text and images with remarkable efficiency
and exceptional quality. Bedrock customers will also be the first to get their hands
on Luma's newest, most advanced visual AI model. To tell us more about the latest innovation, please welcome
Amit Jain, CEO of Luma AI, to the stage. [music playing]
Thank you Swami. I appreciate the introduction and I am very excited to be here today.
Luma's purpose is to build the next generation of intelligence. One that partners with us
and helps us humans do extraordinary things. The future of intelligence is going to be highly rich
and highly audiovisual. To make this possible, we need AI that goes far beyond language models.
AI that sees and understands our world. And it works so fast that it's interactive.
It's like collaborating with AI as a creative partner. Swami announced here today that we are about to bring Luma
AI models to Bedrock. Specifically, our brand new video AI model, Luma Ray 2.
Let me tell you what it is and why you should be very excited about it.
Luma Ray 2 is going to be the most capable and high quality text to image and text to video generation model.
This is made possible by our pioneering new generative model architecture, and it's built from the ground up to make whole new design,
marketing and video creation workflows possible for all of you. As you can see here from these videos made entirely on Ray 2,
it generates highly realistic production quality videos from text instructions or image frames,
as well as videos you've shot. Ray 2 also enables groundbreaking new controls over composition,
colors, camera and actions. This means now you can bring your entire brand identity
into the model and make things that look just right, with a great degree of control.
Ray 2 pushes the state of the art forward in video generation
by creating an entire minute long videos, and it does so with unparalleled character
and story consistency. And for the first time ever, it does so at groundbreaking real time speeds.
Using Ray 2 feels like seeing your thoughts appear in front of you as you're imagining them.
This makes an entirely new class of workflows possible in film, design, and entertainment.
We believe Ray 2 is a huge leap forward in the world of creative AI, and now this family of incredible models
and its capabilities will be available right in Bedrock for all of you to build upon.
Now, let me take you a bit behind the scenes and show how these models were trained.
Our models learn from about 1000 times more data than even the largest LLMs.
To make this possible, we hyper optimize every aspect of our training runs to get the maximum throughput from the compute clusters we use.
This means our workloads demand the absolute max
from the compute resources we work with. In AWS, we have found a cloud provider that understands this
and what it takes to build models that push the frontier forward. We chose Amazon SageMaker HyperPod,
after experimenting with a lot of options across the GPU compute spectrum,
HyperPod has been the most reliable and scalable cluster for us. So we doubled down on AWS and increased our commit
by four times, just about four months after signing on.
To train these next generation of models, everything in the stack has to work very harmoniously.
Everything. GPUs, interconnect, power, networking, storage and software.
They all must work with extreme reliability to create a stable training environment.
Anything short of that means frustration, underutilization of compute, and being slow to market.
We have found AWS infrastructure to be fantastic for this.
Their expertise in running global scale compute shows up in the scalability of HyperPod.
Some of you here already know that as a hypergrowth startup, we tend to execute at incredible speeds.
AWS teams moved at our pace from onboarding to evaluation
to optimizing, and helped us train Ray 2 in record time entirely on HyperPod.
In addition to compute AWS, teams have also collaborated with us deeply on distribution
and go-to-market to bring Luma's technology to customers all across the world.
These new models bring us one step closer to our mission of building the next generation of intelligence
that's creative, rich, and highly audiovisual.
We believe that language models alone do not take us where we need to go.
To pull this future forward for our customers at Luma, we are building large scale training and data systems
that learn from humanity's entire digital footprint.
Today, Luma's models are already being used by fashion designers,
studios, ad agencies, marketing teams, and visual thinkers all around the world in their workflows,
from ideation to production. And soon, you'll be able to try these models right in AWS.
As a vertically integrated research and product company, we train these models to make the impossible products, possible.
Feedback from our very popular products also continuously strengthens our models.
And as users of our APIs, all of you benefit from these invaluable gains.
Thank you Swami for helping and having Luma be a part of re:Invent,
and I invite all of you to check out our brand new models on Bedrock,
and let us build the future together. [music and applause]
Thank you, Amit. I still remember our first time call in the early part of the year
when he was starting to build these models, and it's amazing to see how startups can move at an unprecedented pace
when you have the right tools. Luma AI is truly pushing the boundaries
of video content creation through the power of GenAI. Now, the right foundation model can unlock incredible possibilities,
and with access to the most innovative model providers in the industry, Bedrock is opening up a world of potential
across a variety of use cases and modalities. While these models can support a wide range of tasks,
we know that your interest in emerging and specialized task-based models is growing too.
For instance, EvolutionaryScale’s Frontier language models for biology
are advancing in areas like drug discovery and carbon capture.
Or take IBM's Granite family of models that are accelerating a wide variety of business applications.
Customers told us that they want to combine the power of these specialized models
with all of the developer tools on Bedrock to unlock even greater value for their business.
So today we are doing just that. I'm very proud to announce Bedrock Marketplace.
[applause] Bedrock Marketplace gives you access
to more than 100 emerging and specialized foundation models from leading providers.
Now, you can streamline your development workflows by discovering and testing these emerging and specialized models
through a unified experience in the Bedrock console. And once you deploy these models,
you can use these models with Bedrock unified APIs and leverage our on Knowledge Bases,
Guardrails, Agents and all these capabilities, as well as the security and privacy features
we have built into Bedrock since day one. With Bedrock, we are committed to giving you access
to the best model for all your use cases. However, while model choice is critical,
it's really just the first step when we are building for inference. Developers also spend a lot of time
evaluating models for their needs, especially factors like cost and latency
that require a delicate balance, as optimizing for one typically requires a compromise on the other.
That's because cost and response latency inversely correlate with model accuracy
as more capable, highly intelligent models consume more accelerator hardware.
This week we introduced new features that make it easy for you to find the right balance for your use cases,
including a new model distillation feature in Bedrock that makes it easy to transfer specific knowledge
from a large, more accurate model to a smaller, more efficient one that makes it up to 500% faster
and up to 75% cheaper. We also introduced a latency-optimized inference option
that allows you to have access to our latest AI hardware and other software optimizations
for a wide variety of leading AI models. But we know there are more problems we could solve for our customers
by optimizing the process even further. So let's dive in.
Inference starts with your prompts, which are the inputs and instructions you give to your model to generate outputs.
When you send a prompt to a model and the model responds to your query, it generates tokens,
which you can think of as the fragments of language the model can understand.
The more tokens you send, or longer the prompt, the higher the cost. So when this process is not optimized for your use case,
token generation costs can quickly rise up, especially when prompts are frequently repeated.
For example, imagine a law firm that has thousands of new documents passing through its doors every single day.
Some of the lawyers want to familiarize themselves with the latest status of an acquisition
that their firm is working on, so they ask questions about, like the payment structure or does it include warranties and so forth.
When they ask all of these queries, they require the context contained in these documents.
So they send it as part of the prompt, slowing down the query response time and increasing cost.
We knew we could solve this problem through caching. In this scenario, we are caching the entire document
after encoding the token once so it isn't reprocessed in subsequent prompts,
allowing it to skip past input token processing. We wanted to give customers an easy way to dynamically cache
their repetitive prompts to decrease cost and latency, without having to compromise on accuracy.
That's why today I'm excited to share the support for prompt caching on Bedrock.
[applause] This one is going to be a really big deal when it comes to cost savings,
because with prompt caching, you can not only lower your response latency, but also decrease costs by caching frequently used prompt prefixes
across multiple API calls. To get started, you simply use Bedrock APIs or experiment with playground
UI to see how much it can save for your use cases. With this feature, you reduce your latency by up to 85%
and cost by up to 90% for supported models. Now, in addition to frequently optimizing
these frequently repeated prompts, developers also told us it can be difficult to route their requests
to the right size model for every use case. Some prompts may require advanced, highly capable models,
but some prompts might require actually very simple, fast models.
Today, developers end up spending a lot of time experimenting with various models to find the best fit for each of the use cases.
For example, let's say you manage a travel planning website and you want to select the best models
to tackle a variety of customer questions. Your started by testing a simple query saying like,
can you suggest the best plan for me and my family to visit in December.
And you test it against three models in the same family, evaluating each response for speed, accuracy and cost.
And you find that the smaller, less expensive model A provides the right balance of accuracy and performance.
Now you test a more complex scenario, something like you create a seven-day itinerary
for multiple destinations across Europe with some warm weather, and I want to stay the final day in Paris
to meet up with some friends. You evaluate this query with each model, and then find that the most advanced model,
C, can handle the nuances of this request, and. But it might end up being an overkill for simpler problems.
So now imagine that you have to repeat it for like hundreds of different use cases or possible questions.
To route each request, you would need to hand code which prompts get routed to which models.
And then you have to do this over and over as the customer request pattern changes or new models become available.
We wanted to make it easier to make sure it is easy to route
the optimal prompts to the right model for all your use cases.
That's why today I'm excited to announce Intelligent Prompt Routing, a new capability on Bedrock.
[applause] This feature will route your prompts
to different foundation models within a model family, helping you optimize for cost and quality of responses.
You can simply choose the models you want to use, set up your desired thresholds for cost and latency for each request,
and Bedrock will dynamically route your requests to the model that's most likely to give you
the best response at the lowest cost. In fact, intelligent prompt routing can reduce your cost
by up to 30% without compromising on accuracy. With these features, you can take the guesswork
out of inference optimization across a variety of use cases.
Now, when it comes to building unique experiences for your customers,
the real magic happens when you customize these models with your data.
For doing this, the easiest place to start is retrieval augmented generation or RAG.
With RAG, you enhance your prompts with proprietary data to create better responses to customer questions or requests.
For example, imagine you are running an online computer retailer where customers often ask complex compatibility questions.
A customer asks your GenAI powered chat app about the status of their recent laptop order.
By including data from your order management system and shipping database, you can provide the model with more context to generate
a highly accurate and relevant response. This process of RAG looks really simple,
but in reality it requires a lot of manual heavy lifting right from having to index this data
with the best-in-class embedding models, and then you have to store your embeddings in a vector database.
During the time of generating a response, you've got to create a custom retrieval mechanism
and then augment it and prompt it with the right model. All this process makes it really hard to build RAG, really easy.
We have made it easy to manage the entire RAG workflow with Bedrock Knowledge Bases.
Knowledge Bases is a fully managed RAG capability that enables you to customize responses
with contextual and relevant data. It automates the complete RAG workflow,
removing the need for you to write custom code to integrate your data sources and manage queries.
Customers like Ericsson, F1 and Travelers are using Knowledge Bases to generate more accurate and engaging outputs.
Bedrock Knowledge Bases provides a strong foundation for RAG workflows.
But efficient and highly accurate retrieval for your vast enterprise data sources can be challenging.
This is where Amazon Kendra comes in. Kendra is our intelligent enterprise search service
that uses machine learning to help surface more relevant data. Kendra can also help you create and manage vector embeddings
while leveraging its semantic understanding to enhance retrieval accuracy for your applications.
It also has built-in connectors to more than 40 enterprise sources. Our customers wanted an out-of-the-box vector index
that helps them select the best embedding models, optimize vector dimensions and fine-tune the retrieval accuracy.
They also wanted to seamlessly integrate it with their knowledge bases and across their entire GenAI stack.
That's why today we are happy to announce Kendra GenAI Index.
[applause] This feature provides you a managed retrieval for RAG and Bedrock
that supports connectors to more than 40 enterprise data sources. You can use it as a Bedrock knowledge base
and build GenAI-powered assistants with features like Agents, rompt flows, and Guardrails.
The other cool thing is you can leverage this content across other use cases like your Amazon Q Business applications.
We are making it easy for you to connect all of your data across your enterprise apps,
but we also wanted to make it easy for you to work with more of your data when you are building GenAI apps,
whether it's structured data sitting in your data warehouses or data lakes, unstructured data like documents or PDFs,
or multimodal data that combines image and videos with text. Now let's start by looking closer at structured data.
Companies tend to store all their operational data in data warehouses or data lakes.
However, making structured data accessible for RAG requires more than just looking up a single row in a table.
For example, take a natural language query like what were the most important product categories by revenue in the Washington state last month?
For the warehouse to process this request, you would need to create a SQL query to filter,
join tables and aggregate data. This process – translating natural language to SQL
is as crucial to structured data as vector stores are for documents.
So many of you in this audience might be thinking, Swami, why is this so hard to do? Can't you just prompt an LLM to do this?
In reality, it's not that simple. To do this right, and to do this effectively, you need to implement techniques like customized schema embeddings,
query analysis, data sampling, and query correction loops, all the while addressing security concerns
like prompt injection attacks. To manage these tasks, developers often spend time
building complex custom SQL solutions for accurate SQL query generation.
Today, we are solving this problem for our customers. I am pleased to announce Bedrock Knowledge Bases
now supports structured data retrieval. [applause]
This will unlock so many new GenAI use cases. And this is one of the first fully managed,
out-of-the-box RAG solutions that enables you to natively query
all your structured data from where it resides for your GenAI apps.
You can use natural language to query data in SageMaker Lakehouse or Amazon Redshift,
and the recently launched S3 tables with Iceberg support. Knowledge Bases will automatically generate
and execute the SQL queries to retrieve your data and then enrich the model's responses.
The cool thing is, it also adjusts to your schema and data, and it learns from your query patterns
and provides the customization options for enhanced accuracy.
Now, with the ability to easily access structured data for your RAG, you will generate more powerful and intelligent GenAI
applications in the enterprise. However, as many of you continue to build RAG applications,
we know that your expectations for relevancy and accuracy have only increased.
Producing relevant responses with RAG is especially challenging because information is not contained in a single document,
and it's usually dispersed across multiple sources or multiple documents.
For example, let's take a customer scenario where a customer contacts their online retailer
about a malfunctioning smart home device. The online assistant now needs to quickly connect
multiple pieces of information, like customer’s purchase history and then their previous tickets, and then the product details
and the relevant knowledge base articles. But then it struggles to link all these various data sources
to provide a tailored, relevant response. To solve for this, what you really need
is something like to capture all this information in a knowledge graph. Knowledge graphs create relationships between your data
by connecting different pieces of information, like a web would do. In this case, the customer represents the node
which connects to their purchase history via a purchase stage and the supported tickets via submitted edges.
When these relationships are converted into graph embeddings for your AI applications,
the system can easily traverse this graph and retrieve these connections to gather a holistic view of your customer data.
With the knowledge graph, the system is now able to connect the recent purchase to a known issue,
find relevant support and suggest a solution. However, building a RAG system with a knowledge graph
requires a high level of expertise. Developers need to spend additional time
writing custom code to integrate their graphs into their RAG powered applications,
then augment their prompts to create more relevant response. We knew we could make this entire process easier for you.
That's why today I'm very excited to announce Bedrock Knowledge Bases now supports GraphRAG.
[applause] This is a brand new kind of capability,
which automatically generates graphs using Amazon Neptune and links the relationship between various data sources,
creating more comprehensive Gen AI applications without the need for any graph expertise.
Knowledge Bases can also now enhance explainability by making connections and source information explicit
for better fact verification. With the support for GraphRAG, customers can now generate more accurate responses
for their applications through a single API call. Finally, let's look at some of the challenges developers face
when they are working with multimodal content for AI. Most enterprise data is unstructured,
contained in multimodal content like documents, videos, images, and audio files.
Wouldn't it be great if you could easily leverage this data for your GenAI applications?
Unfortunately, unstructured data is difficult to extract and it needs to be processed and transformed to make it ready.
Let's take a look at a couple of examples. Let's say you work at a streaming service, and you want to develop an application
that intelligently places relevant ads within TV shows and movies.
To do this, you need to first index all of your videos by analyzing hundreds of thousands of hours of content.
In parallel, you would also need to index all your ads and match relevant ads and place them at the perfect moment
to provide a better viewer experience and deliver higher ROI to your advertisers.
Or let's say you work at a large bank and want to build an automated loan approval
workflows to leverage unstructured data within each loan package. Now you need to separate and classify each document in a packet.
Then you have to extract, normalize, and transform the data before loading it into your database.
Now, regardless of your industry or vertical, I'm sure most of you are familiar with this process.
In the database world, it's called ETL. We wanted to make it easier for you
to leverage your multimodal content for GenAI. That's why today I am thrilled to announce Bedrock Data Automation.
[applause] This feature automatically transforms your unstructured,
multimodal content into structured data to power your GenAI applications – no code required.
I like to think of this as a GenAI-powered ETL for unstructured data. This feature will automatically extract, transform,
and process all your multimodal content at scale. With a single API, you can generate custom
outputs aligned to your schemas, parse multimodal content for your GenAI applications,
or simply load these transformed data to power your analytics. Bedrock Data Automation helps mitigate
the risk of hallucinations as well, because it provides confidence scores and grounding
the responses in the original content. Customers are already seeing success with this feature,
like Symbeo, a CorVel company which offers automated claim processing solutions.
With this feature, Symbeo is streamlining this process for extracting and transforming insurance claims and medical bills
into application data, enhancing claims efficiency and reducing the customer turnaround times.
With these updates, we are empowering you to harness all of your data to build contextually more aware GenAI applications.
However, as GenAI continues to transform across a variety of models and data types,
it can be difficult for developers to ensure they have the right safeguards in place.
That's why we offer Bedrock Guardrails, which enables you to implement configurable
safeguards for your applications. Guardrails helps you block up to 85% more harmful content
than the protection natively provided by the foundation models on Bedrock,
with content filters that can detect and block harmful text content like violences and insults.
It also offers contextual grounding checks to detect and filter hallucination.
And this week we announced new automated reasoning checks. Now, Bedrock can check whether factual statements
made by your models are accurate based on sound mathematical verifications,
and show you exactly how it reached that conclusion. But as more of you leverage the latest multimodal models
for your use case, you need to account for potentially harmful content contained in your unstructured data, too.
That's why today I'm pleased to announce multimodal toxicity detection for Bedrock Guardrails.
[applause] This feature expands Bedrock's configurable
safeguards to support image data, enabling you to build secure, multimodal GenAI applications.
For example, an online ads classified company can now prevent users from interacting with potential toxic images
content like hate, violence and misconduct. This update is available for all models in Bedrock
that support image content, including the fine-tuned models.
Now, all of the tools and challenges we have touched on so far, from model choice to responsible AI
will become an increasingly important part as more of you leverage these FMs to solve problems
and take action on your behalf, just like AI agents do.
Agents move us beyond passive language understanding to active reasoning and multi-step problem solving,
unlocking new levels of automation that were not possible before. They are designed to achieve specific objectives,
and they are able to break down complex tasks into manageable steps, much like an experienced professional would.
Let's take a look at an example. In addition to being a great mom, my wife is a trained pastry chef
and has impeccable standards when it comes to food. So I take finding the best restaurant very seriously.
But the ex-grad student in me always tells me, you know what's better than amazing food, amazing free food?
And at a large conference like re:Invent, it can be incredibly difficult to figure out
where to find the best food at all of the sponsored events and parties. So let's see how a multi-agent workflow can help you find free food
before your hunger turns into hanger. The first agent gets your food preferences like I want Italian
and I can't eat meat or seafood. The next one analyzes conference events to determine
which restaurants are hosting parties, and the third agent gathers details about the restaurants and sponsors
to help you decide which party to attend. The fourth agent tells you when the party starts,
and estimates how long it will take for you to get there, and then your final agent takes all your conference information
to automatically register you for the event. As you can imagine, in this fun example,
agents that are available are able to take action on your behalf can be extremely powerful.
To help our customers easily deploy their own agents at scale, we offer Bedrock Agents.
Bedrock Agents provides advanced AI components that are purpose built for orchestrating
and automating complex workflows. They combine language understanding capabilities of these FMs
with the reasoning and execution abilities, decomposing these high level goals
into sequential steps and planning required. And as of this week, Bedrock Agents now support multi-agent collaboration,
making it easy to build and coordinate specialized agents to execute complex workflows.
Customers are using Bedrock Agents to create more innovative and relevant experiences,
including the PGA Tour, who use Bedrock Agents to convert real time data and insights into engaging commentary
that can be tailored to the preferences and the language of individual fans.
This personalized, AI-powered solution represents just one way you can leverage
Bedrock's comprehensive suite of capabilities, right from choosing the right model to optimizing your models
to customizing models with your data. All the capabilities you need to build with GenAI
have converged on Bedrock to simplify the developer experience and empower organizations to fully unlock the power of AI.
Now, I'd like to introduce a customer that's tackling several of these areas,
from RAG to agents to drive transformation in the mortgage and financial services industry.
Please welcome Shawn Malhotra, CTO of Rocket Companies, to the stage.
[music and cheering]
Thanks so much. So look, I joined Rocket just under seven months ago.
It's only the second time in my 20-year career that I've switched companies. So there had to be a compelling reason for me to make that leap.
Now, there were lots of great things to love about Rocket, but what I ultimately made my decision
on was the opportunity I saw to use cutting edge technology
to service an incredibly worthy mission – to help everyone home.
The home ownership is a cornerstone of the American Dream. But the journey to achieve that dream is still riddled
with friction and stress. In fact, 60% of millennial and Gen Z homebuyers experience
tears of frustration during the process. Sounds more like a nightmare than a dream.
And when you dig deeper at the mounds of paperwork, the manual processes, the lack of deep personalization,
you realize that many of these pain points are solvable if we just use the right data in the right modern tools
like generative AI. For years, Rocket has been a trailblazer in our industry.
We were the first to take mortgage to the internet, the first to take mortgage to mobile,
and now we're taking it to a whole new levels with AI.
This is an industry begging to be disrupted. And with our ten petabytes of data, our 360 view of a client
throughout the entire homeownership journey, with our incredible talent, and by working hand in hand with AWS,
that disruption has started. But it's just the beginning. It's just the tip of that iceberg.
Now AI isn't new to the world or to Rocket. We shipped our first AI models a decade ago back in 2012.
Today, we have over 210 proprietary models out there in production.
But we've entered a new era of AI. And it's not just hype. Even though I'm a CTO,
generally a little skeptical of the shiny new thing and potentially unrealistic expectations,
but this is different. This is the technology that's going to make it impossible
for my kids to relate to me and my wife. And it's coming fast.
We at Rocket know that if we want to lean in and meet this moment for our clients,
we've got to partner with the world's best like AWS.
AWS teams from the AWS Executive Briefing Center, the GenAI Innovation Center have played a critical role as our allies,
helping us navigate this transformation. They've helped us design and build scalable, intelligent solutions
that are tailored to our industry and our clients. They've allowed us to work together as we define frameworks
to leverage new concepts like the orchestration and creation of AI agents. Like many of you, we love AWS's approach
of working backwards and experience-based acceleration. Those methodologies help us innovate way faster,
way more effectively, and solve some of the fintech industry's thorniest problems.
I mentioned earlier that GenAI isn't just hype. So I want to talk about some real results
it's driving for our business and clients today. At the heart of it is our patented AI driven platform.
It's the base off of which we've been able to build so many of our AI experiences, and it's powered by Amazon Bedrock, and AWS.
That tight collaboration has been essential to our success. Now, one example of something we built off of that platform
is our AI-powered agent feature that guides clients through their homeownership journey. You can chat with that personalized agent right now,
but don't do it right now, wait until after the keynote, but when you do, and I hope you do, if you're like 80% of our clients,
you'll prefer that to a phone call. And you'll be three times more likely to close the loan with us.
Those are big numbers. They show you how you can turn buzzwords like agentic AI
into real value. You can see in this example how we're helping a first time
homebuyer navigate that journey towards her dream. Handling 70% of her interactions autonomously.
All that time saved allows our team to focus on her, answer her more personal questions, better understand what she needs,
really delivering a truly human-centric experience with a huge assist from AI and Amazon Bedrock.
By leveraging our AI platform powered by Bedrock, we've automated tasks, things like document processing,
note taking, sifting through dense mortgage documentation to answer questions, and so much more.
So what has that meant for our business and our clients? Well, a few examples. It's improving first call resolution by 10%.
And in some parts of our business, it's reducing the time required for clients to get their answers by 68%.
That's real value. Those are real people being helped. And hopefully it means a few less tears are being shed
by the homeowners we're serving. GenAI has also had another profound impact.
It's democratized innovation. We've built an internal no code tool that we call Navigator,
which allows everyone in the company, not just technologists, to access a wide variety of the world's best LLMs.
It lets them leverage AI patterns like RAG without even having to know that it stands for retrieval augmented generation.
It can auto-generate database queries to allow our business partners to get deep and complex insights out of our data,
without having to involve a tech team. That has unlocked the imagination of the entire company.
And it's upped our pace of innovation. Since launching in July, after just a few months of development,
we've had 2400 team members use the tool, driving 68,000 interactions with an LLM,
and our users have developed 133 custom apps. And you guessed it, it's all made possible by Bedrock.
What took us just a few months to build would have taken so much longer without it.
Overall, we've seen a ton of business value with AI powered by Bedrock. We've driven efficiency. We've enhanced client experience,
and we've been able to quickly scale AI to multiple products and experiences in a matter of weeks and months,
not months and years. When you add it all up, it comes to 800,000 team member hours
that we're saving each year. That allows them to focus on what they love to do,
deeply understand our client's dreams, and help them achieve them.
I want to thank our AWS team. They've been with us every step along the way. Both of our organizations have innovation
and entrepreneurship in their DNA, which has made working together so easy. At Rocket, we have a set of foundational values and principles.
We call them our isms. A few of them really describe the way we've approached our journey here together with AWS.
Obsessed with finding a better way and innovation is rewarded, execution is worshiped.
We've been relentless in figuring out how to transform the home ownership journey with AI,
and then delivering real results to back up that vision. We've made a lot of progress, but we're just getting started.
We're working on some really big things with AWS, like bringing real time, context aware personalization
to that client-facing AI assistant that you just saw. And as we continue to push the boundaries of what this tech can do, it's going to be incredible.
We're not going to stop until buying a home is as easy as, say, buying a book online.
And then we'll know we're truly delivering on our mission to help everyone home.
Thank you. [music and applause]
Thank you, Shawn. You know, I love seeing how Rocket Companies is putting together
these technologies to work for their business, especially as we look towards the agentic future,
these agentic systems will be critical for getting our jobs done faster,
which is why we offer tools like Amazon Q. Q enables you to quickly get started with AI
to accelerate productivity across your workforce. From developers to data analysts to business users,
it's powered by Bedrock under the hood, with powerful foundation models and agentic capabilities
that help you tackle complex problems with a clear purpose and direction.
Take Amazon Q Developer, your AWS expert, and the most capable GenAI assistant for software development.
Yesterday, Matt discussed how Q can help you across the entire end-to-end development lifecycle,
right from code generation and end-to-end feature development, to writing tests and creating documentation
to accelerating legacy application transformation to streamlining development tasks and debug operational incidents.
We have made incredible progress with Q Developer to date. In fact, Q’s agent for software development
is now the highest performing on the verified leaderboard for SWE Bench.
Now, today Q is able to solve 54.8% of software development problems
in this highly popular benchmark, which is like a standard when it comes to solving advanced coding problems.
And this is more than double the amount of problems Q could solve when we first topped the leaderboard
just seven months ago. I'm astounded at the pace of improvement here by the Q team,
and so are our customers. In fact, customers like DFL Bundesliga,
United Airlines and BT Group are using Q for code generation, platform consolidation, and Java upgrades.
So when we first launched Q, our primary focus was on enhancing productivity
across the traditional software development life cycle. However, as we explored its capabilities more and more,
we quickly realized that its potential extended far beyond your day-to-day development tasks.
We also saw enormous potential for Q to help you build your ML models faster.
Building a model requires a high degree of ML expertise, and it involves a series of time
consuming tasks like feature selection and feature engineering, choosing the best algorithm and then training them,
hyperparameter tuning and evaluating the model. While we have made it easier to tackle the entire ML workflow
and build ML models with tools like Amazon SageMaker Canvas, we knew we could use the power of GenAI to do even more,
especially for customers with little experience in ML model development.
That's why today I'm excited to announce Q is available in SageMaker Canvas.
[applause] With this capability, even if you have not written a single line of Python,
you can simply state your business problem in natural language and queue will walk you through the process of building an ML model.
For example, let's say I work in the manufacturing industry and I want to build a model to predict
whether a product will pass or fail in production quality test using our data sets in the SageMaker catalog.
Q will give me a step-by-step guide that will help me break down the problem into a series of tasks.
Then it will help me prepare my data, define the ML problem, and build, evaluate, and deploy the model.
I'm excited to see how this feature helps more of your ML model development.
But we designed Q to be a lot more than an assistant for developer tasks and ML workflows.
It also empowers business users with two GenAI powered assistants to get their jobs done faster.
The first is Amazon Q Business, which helps employees easily connect to data and information stored in their enterprise systems.
Q Business creates value quickly for organizations by answering questions, providing summaries,
and even generating content to enhance employee efficiency. For example, the NFL used Q to create a GenAI
assistant for their producers, editors, and creators to accelerate content production.
This solution reduced their new hire training time by 67%,
and employees can get answers to their questions in 10 seconds rather than up to 24 hours.
Think about the productivity improvement. In addition to Q business, we are helping business users
accelerate data-driven decision making with Q in QuickSight. Q in QuickSight delivers insights to more users with the power of AI.
Q provides natural language executive summaries of dashboards and enables you to ask questions about your data
and get response with a multi visual chart and graphs that help speed up decision making.
Customers are using Q in QuickSight to unlock business insights across a wide variety of industries
and use cases, including the Formula 1 racetrack. During the Formula 1 engine assembly,
Scuderia HP recognized opportunities to democratize access
to huge volumes of data to help their engineers get better insights.
With the dashboard authoring capabilities in Q, engineers can use natural language
to spin up dashboards and spot anomalies right during the manufacturing process.
The convergence of business intelligence and generative AI with Amazon Q will continue to unlock new possibilities for our customers.
But as these models became more and more powerful, we knew that we could do more here
to accelerate data-driven decision making. Today, many business users are faced with questions
that cannot be directly answered by a simple Q&A on their data.
I personally experienced this when I was launching DynamoDB like ages ago,
and we were trying to decide what an optimal free tier duration would be.
Our big question was quickly turned into many smaller questions, each of which required to find data
and in some cases create hypothetical scenarios to solve the problem.
For example, to determine our cost per user, we had to combine infrastructure costs with usage scenarios
that require deeper analysis for every option. While the launch of DynamoDB is now history,
this problem still persists for business users today that spend hours or even days on tedious analysis
among various spreadsheets. We knew that Amazon Q could make this kind of scenario analysis
easier for our customers. That's why today, I'm excited to announce the preview of Scenarios in Q in QuickSight.
[applause] This is an exciting capability which business users can ask you
to help solve complex business problems using natural language. Q will just find the relevant data,
suggest analysis, plan each step and execute the job, providing detailed insights and suggestions each step of the way.
With this feature, business users can now perform these analysis up to ten times faster than traditional spreadsheet-style analysis tools.
Let's see how it works. I can describe a scenario like, what is the optimal free trial duration?
Now Q searches all my dashboards for relevant data and prepares it for analysis.
It automatically breaks down the problem into smaller questions we want to answer.
I can choose a question to analyze, and while this analysis starts, I can add more.
For example, I can ask what if all trials were 30 days and add a hypothetical scenario
to explore the impact free trials have on revenue?
I can easily modify the analysis, for example, removing direct buys
that show up as zero day trial by asking Q to ignore these results
and these records and get an updated answer. Each answer makes it easy to get the data and insights
I need to make informed decisions, like the variation in the conversion rate across trial duration,
or the insight that the longer trials will reach a point of diminishing returns.
And as we work, Q takes into account each step, enabling us to see how we arrived at an answer and make changes as needed.
Q in QuickSight Scenarios will dramatically accelerate business analytics.
But the convergence of tools, data, and AI is not only unlocking insights for customers using Amazon Q.
Enabling fast SQL analytics and big data processing on your data lakes, accelerating model training on SageMaker AI
and sparking new GenAI powered experiences on Amazon Bedrock,
which are all coming together to streamline your entire analytics and machine learning workflows with the next generation Amazon SageMaker.
To demonstrate how we are empowering you to leverage all these innovations with Amazon SageMaker,
please welcome Shannon Kalisky to the stage. [music and applause]
All right. Thanks, Swami. 1,330,432GB.
That's approximately how much data is in this room right now.
And that's if we're only counting cell phones. We are surrounded by data.
And in almost every task we can see the convergence of data, AI and analysis growing.
But we also see the complexity that comes with it, the frustration of hunting for the right data
set and switching between consoles just to get a job done, and the challenge of collaboration.
But what if we could bring order to the chaos,
make it easy to find the right data, get all the tools you need in just one interface,
and seamlessly collaborate with others. With the next generation of Amazon SageMaker, we can.
Let's take a closer look and imagine that we are data workers at a robotics startup,
and our task is to increase sales. Just the kind of big ambiguous problem
data chaos loves. But do you know what?
Bring it on. We want to increase sales. Well, then we'll want to increase leads.
So let's take it end-to-end. Step one – drive more leads.
That one seems obvious. Step two – analysis. Yes, very logical, love it.
And step three – we want to prioritize those leads. We need to know which ones to go after.
Let's see how the new SageMaker Unified Studio can help.
Now we're going to start with step one. And despite what this room and the live stream
may lead you to believe, we are actually a very small team,
so we will create a chat agent to engage with customers on our website
and automatically generate sales leads. To get started, we will launch the generative AI playground.
Here we can compare models side by side and ask them prompts we think our customers would,
like I want to learn more about packaging robots,
and this allows us to see which model will best meet our needs. And when we find the one we like, we can start building
our AI assistant in the Bedrock IDE. Here we can create Guardrails, add Knowledge Aases,
and create that function to generate leads. All we do is give our function a name,
describe it, and integrate a schema to integrate with our CRM.
Here we can see we have integrated it with our CRM and then when we're done, we will export it
so that it can be embedded in our site, where it can start helping customers and generating leads that sales can follow up on.
So, fast forward, we're in the future. How else did you all think we would get there, guys?
Our AI assistant is now generating hundreds of leads per day,
and we want to analyze that data. We can use the new Zero ETL for applications integration
to bring our data from our CRM back into SageMaker, so a data analyst can work with it.
So this brings us to step two – analysis. We need a way to group the leads so that they're easier to prioritize.
To do this a data analyst will combine the leads with other data sets and create customer segments.
But before they do, they have to find the right data. And in SageMaker, you have two options.
You can search using the data catalog for example leads.
And this will match on keyword and semantic meaning. Or you can use Q and ask questions like,
where can I find the data set that contains the leads generated by the AI assistant?
Q will find the data that we need to generate the results,
let us preview that information, and if we want to work with it we just subscribe.
Then to start our analysis we will launch the query editor –
there it is – where we have access to the data we've subscribed to and can choose if we want to query the data with Redshift or Athena,
and then start building the segments. We'll explore market data, technographic data
and conversion rates, looking for patterns, and then combine all of those into a combined data
set where we'll save our segment definitions. And then we'll write all of that back into the Lakehouse
so it's available to our collaborators. All right, step three.
We need to figure out which leads to go after. And to do this a data scientist
is going to create a machine learning model to score and prioritize the leads as they come in.
In the past, this would almost certainly require multiple notebooks.
We would probably start by preparing and pre-processing our data in EMR
and then jump into SageMaker where we're going to build and train the model. But now, we can do everything from a single notebook
by applying the compute we want to the code that needs it.
Now as we build out this model we're going to want to try different methods to see which one works best.
We can use Q to generate the code we need, such as a model that uses random cut forest to score leads.
Once the code generates, we can easily add it to our notebook.
And from within SageMaker we can train and deploy the model so it's available for inference, scoring new leads as they come in.
But for this to be truly useful, sales needs a way to act on the results.
So we will write those results back to the Lake House, which allows other AWS services to access the data
so it can be visualized in a business dashboard. Now, every day when sales logs in, they see the top leads to go after,
which helps them close more deals and helps us increase sales.
So take that, data chaos. With the next generation of SageMaker,
you get everything you need in one place, enabling you to solve complex end-to-end problems collaboratively
without the complication of disjointed data systems. This next generation of SageMaker is available in preview today.
I can't wait to see what you do with it. Thank you.
[cheering and applause]
[music playing]
Thank you, Shannon for the lively and lovely demo. So, you know, we were practicing backstage this jump.
Maybe we will do it later. I'm excited for all of you to take advantage of this new and unified platform.
As you can see, technology is powerful, but I would argue that technology alone is not enough.
It's how we apply it at the right time and the right environment that truly makes a difference.
This reminds me of a fascinating concept from Malcolm Gladwell's book, The Tipping Point.
Gladwell explores how the surrounding conditions, like context, can be crucial in determining
where an idea or an innovation takes off. It's not just about having potential, it's about that potential existing
in an environment that's ready to nurture and amplify it. Think about this context in your own career journey.
What were your personal tipping points? The moment where the context was just right for your growth and success?
Perhaps it was when you had a manager who believed in you and gave you those challenging projects.
Or maybe it was when you joined a company with a culture that encouraged risk-taking and innovation,
like I experienced at Amazon. This concept is something that deeply resonates with me,
especially when I think about education. Just as we all needed the right context to thrive in our careers,
students need the right environment to flourish in this era of GenAI.
However, on a global scale, we know that accessing quality digital learning opportunities continues to be a challenge.
According to UNESCO, half a billion students worldwide couldn't be reached by digital learning,
with most among the poorest and rural areas. That's why AWS has a long standing commitment
to advance education and empowering these learners from diverse backgrounds.
Our AI-ready initiative, which we announced in 2023, has already hit our goal of training more than 2 million learners
globally with free AI skills. Our AI and ML scholarship program has provided $28 million in scholarships
to help underserved learn. Cutting edge AI technologies. And our Amazon Future Engineer Program
has provided $46 million in scholarships to future builders
from underrepresented communities. And I am thrilled to announce that we have achieved our goal
of providing free cloud computing skills training to 29 million people globally.
A full year ahead of our 2025 target. That's a big deal.
[applause] But these are not just numbers.
Behind each statistic is a story of transformation and impact. AWS, AI and ML Scholarship recipient
Prerana Sapkota is using AI to combat water scarcity in Nepal
and Gedeon Baende is developing an AI solution to help identify second life
applications for electric vehicle batteries, paving the way for a more sustainable technology use around the world.
In fact, Gedeon is actually here with us in the audience today, and I want to take a moment to recognize his amazing work.
I'm incredibly proud of individuals like Gedeon and all that we have been able to accomplish with AI education,
but we know there is still more work to be done. The scale of today's AI education gap demands innovative solutions,
and leveraging AI solutions is crucial to expanding access.
Many organizations, like those in the education technology sector, have learning visions that are ready to be implemented and deployed,
but limited funding prevents them from executing on these plans. We know we could help these dedicated organizations
reach even more learners worldwide. That's why today I'm excited to announce
AWS Education Equity Initiative. [applause]
This initiative will empower organizations to build and scale digital learning solutions for underserved learners worldwide.
We are committing up to $100 million in cloud computing credits and provide the technical guidance from AWS experts
over the next five years to make this vision a reality. This initiative will help reduce the financial barriers
and the right technical guidance they need, so that their organizations can build and scale their education solutions
like providing architectural guidance, best practices for AI and responsible AI implementation,
ongoing optimization support. With this initiative, we are also excited to build
on our long standing partnership with Code.org. Over the past decade, AWS has supported Code.org
in scaling their free computer science curriculum to millions of students across 100 countries.
And now, with the help of this initiative, Code.org is using Amazon Bedrock to automate student project assessments,
freeing up hundreds of educator hours that can now be spent on individual instruction
and tailored learning experiences. This initiative will also empower Rocket
Learning, an organization dedicated to early childhood education in India
to enhance learning outcomes for more than 3 million children using Amazon Q in QuickSight.
Here, Q helps them optimize the type of content they need to make available for children in a diverse
set of regions across different languages with different nuances.
With Chennai, we can amplify the impact of organizations that are already doing incredible work at a global scale.
But even here in the US, students can often fall through the cracks. Let's take a look at another company that's empowering educators
to improve student outcomes using Q. As a former first grade teacher,
teachers are counselors, teachers are support systems. Teachers are really everything to students.
But this struggle can be time between class. You have a ten minute period to make any adjustments
and pivot with any instruction based on data. That can range from attendance to tracking discipline
to visits to the nurse. Assessment grades can be very overwhelming.
But AWS in the cloud were really critical to digitize all of that and bring it together into one central repository.
SchoolTool is a student management system used by more than 400 school districts across New York State.
With AWS, we've really been on a journey to get to insights by leveraging GenAI.
With GenAI, it's really a tectonic shift. Before Q in QuickSight, educators had to spend weeks
to work with their data engineer to grab data out of a system. Now, with the power of Q in QuickSight,
that individual can just ask a simple question, in plain English, in text, and receive an immediate response.
For example, how did my students perform last year versus this year
and have effortless data visualization? They can build their own dashboards.
You can really start to create your own command center, so to speak.
That enables every single individual across the school district to get the answers that they need when they need it.
The power of GenAI and Amazon Q is to allow teachers to be able to get more comfortable with data.
You fully democratize data analytics right to the end user. Being an educator is one of the most challenging yet rewarding jobs,
and having the data at your fingertips is going to make your students that you're impacting more successful.
[music playing]
It's inspiring to see how all of the technologies we have discussed today are actively transforming our students,
our customers, and even the world. From powerful tools for training foundation models
at scale to GenAI assistants that are revolutionizing productivity, we are all active participants
in this historical moment of convergence, building upon the dreamers that came long before us.
And by paving the way for the next wave of technology pioneers, we are not just shaping our present,
but we are also laying the groundwork for new innovations to take flight. I want to take a moment to personally thank you,
our partners and our amazing teams that built all these capabilities.
For all your hard work to drive this exciting transformation forward. I can't wait to see what you do next.