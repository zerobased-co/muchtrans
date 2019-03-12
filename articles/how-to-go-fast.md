title: How to go fast
source: https://quii.dev/How_to_go_fast

#  How to go fast 

[ ![quii profile image](https://res.cloudinary.com/practicaldev/image/fetch/s--I4Bh1XF---/c_fill,f_auto,fl_progressive,h_50,q_auto,w_50/https://thepracticaldev.s3.amazonaws.com/uploads/user/profile_image/61881/0c870cae-d5c4-4603-ac34-8d6eb02ab1fa.png) Chris James ](https://dev.to/quii)

This article is for anyone who works in software and wants to keep life simple, less stressful but still keep their employer happy. You'll see how by making simple choices and sticking to well-understood, proven principles you can ship software and not burn everyone out along the way.

The business have arbitrarily given your team a year to make _a website thing_ and they've got many grandiose ideas. Don't be tempted to spend lots of time planning up front imagining big architectures and backlogs around all this ambition. This is the path to failure, premature optimisation and broken promises. 

The only promise you'll make is you will showcase what you've done every 2 weeks and accept steering from the business on _actual problems_ and not feature decisions. 

We know going fast is important but so is the quality of the system we're making and the mental health of our team. **We will go really fast but we will always be doing it in a sustainable way.**

We don't want to be stressed out about big-bang releases, having to do big scary refactors or obsessing over irrelevant estimates for work that we may not ever actually do.

##  Iterate 

Start with hello world, fully deployed with continuous delivery. 

**We always want a small and focused vision for the team to be working on.** Developing small things is easy and likely to succeed.

Thinking about delivering tons of features causes teams to over-complicate and makes decision making difficult. 

With lots of features up in the air there's the temptation to expand the team and this also slows things down. [See: The Mythical Man-Month](https://en.wikipedia.org/wiki/The_Mythical_Man-Month)

Instead we work on the next most important thing, based on business expertise, research, developer know-how and feedback from our users. 

We will carry on continuously delivering small features iteratively indefinitely. 

##  Rules and principles 

###  1 Small co-located team 

Small teams deliver quicker than big teams because the lines of communication are small and the amount of work being done at once has to be small. Large teams working on lots of things breeds confusion and complexity.

Having multiple small teams working on clearly separated things _can_ work but requires good coordination. It's a lot easier to define those teams on architectural lines once you have a mature product. I think it's a mistake to take a _new_ project with lots of unknowns and try and divide it amongst many teams because the architecture needs to be very flexible at this point and therefore the teams _wont be able to work independently, they will be coupled_.

In my experience being able to very easily talk to someone is important. The informal chats you have by just turning to your colleague is invaluable in breaking down the barriers of sharing ideas and building relationships. To me this is why I prefer to work in a co-located team because it minimises friction in communication.

###  Pair programming most of the time 

Pairing helps you to write better software and helps cross-pollinate skills, ideas and domain knowledge. It will help grow your team and will improve relationships which will in general make everyone happier! 

Don't mandate it from 9-5 though as it becomes very tiring very quickly. People need time and space to think. 

###  No branches and no pull requests 

You have a small team that are pairing. You _should_ be talking to each other all the time so you don't need pull requests to check code is OK. You're better off shipping it and getting feedback. You should be able to trust two people to get things right most of the time. 

Pull requests are great for open source projects where you don't have implicit trust in every contributor. In a small team you don't need it and you need to take advantage of very tight feedback loops by reducing ceremony in writing software. 

A big theme of these rules is removing barriers to feedback loops and this means we can change software easily. Someone shipping code that isn't ideal **is not the end of the world, just fix it and move on - don't introduce complicated processes that slows everything down**

###  Have a minimal deployment pipeline 

Maintaining pipelines and various non-live environments can become burdensome. At least at the start of the project all you really need is:

  1. Run tests
  2. Deploy to live
  3. Run smoke tests



If you find yourself trying to justify a non-live environment ask yourself

  * What is it that I cant test locally or in production? Why?
  * What are the costs and ramifications of being only able to test a thing in a particular environment?
  * What delays does this cause to shipping to production?



Most of the time you probably wont have good answer to these questions.

###  Continuously deliver to live on green builds. 

This gives you: 

  * Fast feedback
  * Force you to automate tests
  * Force you to write actually shippable code
  * Forces you to have good monitoring
  * Makes releases a stress-free, non-event



[This has been written about a lot](http://www.quii.co.uk/Why_you_should_deploy_on_Friday_afternoon). 

[![Accelerate book cover](https://res.cloudinary.com/practicaldev/image/fetch/s--5XfPWV0j--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://images-na.ssl-images-amazon.com/images/I/41TLwbsl8eL._SX329_BO1%2C204%2C203%2C200_.jpg)](https://res.cloudinary.com/practicaldev/image/fetch/s--5XfPWV0j--/c_limit%2Cf_auto%2Cfl_progressive%2Cq_auto%2Cw_880/https://images-na.ssl-images-amazon.com/images/I/41TLwbsl8eL._SX329_BO1%2C204%2C203%2C200_.jpg)

[And is proven to be how high-performing teams work](https://www.amazon.co.uk/Accelerate-Software-Performing-Technology-Organizations/dp/1942788339)

Manually shipping a week or two weeks worth of work takes time and is risky; releasing small things constantly is easy and less risky. 

###  Write tests 

They enable you to iterate quickly with confidence. Cant do continuous delivery without them and you cant go fast if you have to manually check things all the time.

###  Monolith, not microservices 

Writing distributed systems is a pain in the arse and I'd rather avoid that pain until I actually need to distribute my system. YAGNI in other words. 

Refactoring in-process method calls is far easier than changing API calls. Deploying one application is much easier to deploy than orchestrating many system deployments etc etc.

I've worked on microservice projects in the past but my last project was a monolith and we moved so much faster because we cut out a huge number of issues to contend with.

In order to do microservices you have to think _how_ you will break your system up into small components which leads nicely to...

###  Don't design up front 

Just ship some code, if you make something useful and keep refactoring and iterating a design will emerge from _reality_ rather than developers arguing over a whiteboard.

###  Refactor continuously 

Bad code makes you go slow. Bad code tends to get worse. So refactor continuously, don't have a refactor sprint or something dumb. Don't ask for permission, if it's bad just fix it. 

Half the perceived problems of monoliths come from people writing bad code. If you maintain the quality of the code _real_ abstractions based on _real usage_ will emerge and then if you need to break up your monolith there will be obvious ways to do. 

###  Avoid writing an SPA, embrace progressive enhancement 

SPAs bring a mountain of complexity that most projects don't need. You're probably not building Gmail so stop pretending you _need_ to write an SPA. You can get React on your CV at 10% time.

Instead prefer to use progressive enhancement techniques by writing semantic HTML, decorated with CSS and a sprinkle of JavaScript to enhance the experience a little when necessary. Even better, don't write _any_ client-side JavaScript if you can.

###  Don't obsess over pixel-perfect design 

Writing HTML and CSS can be challenging and very time-consuming if you have a designer being overly precious about their design looking pixel perfect in every browser.

We are writing code for _users_ not designers and most of the time they wont care if it looks a bit different in Firefox compared to Chrome. 

Save time, effort and stress by challenging what is good enough for your users. 

**Simple designs are simple to implement, elaborate designs are complicated to implement**. If your designer is giving you difficult to implement web pages, remind them we're trying to go fast.

###  Ship the first 80%, polish it later 

Related to the above it is a total waste of time to really perfect a certain feature in respect to design and UX if it turns out that it is a feature that isn't needed. 

I have seen a team spend weeks polishing a search feature on a website in respect to its design and its JavaScript only for it to be thrown away a few months later because the fundamental idea was wrong in the first place. 

_Ship enough to get feedback and prove the idea_ , once you've done that you can then spend time polishing it. 

###  The people who write the software are the ones that are on support for it 

This responsibility must be coupled with the empowerment to make the system maintainable. 

If the people creating the system are the ones who have the threat of getting called at 3am because it is down they are more likely to ship more robust code.

###  Use mature, proven tools 

It doesn't matter if you go fast with _shiny thing_ if you then leave and no one can build or understand your code anymore. 

Get a consensus in your team of what you'd all enjoy writing with that is appropriate for the task at hand. Don't pick up a new programming language that is unfamiliar to everyone - remember we're trying to go fast.

###  It must be simple to build the software 

There should be a minimal amount of setup required to run and test the project. It is totally unacceptable to be unable to build a project just because it hasn't been touched for a few months or a key person has left. If it takes an individual more than an hour to setup the project you have failed hard.

With technologies like Docker it is trivial to configure a project so it has all it's 3rd party dependencies such as databases available locally.

It should not be reliant on a particular setup of a computer (beyond installing a few key things such as the JVM, Go or whatever). It must not be reliant on a 3rd party system for it to run & test locally.

To help enforce this, configure whatever CI tool you are using to automatically build the software every morning; even if no one has committed to it. 

###  If the build is red, stop 

The tests must always be passing. If you have unreliable tests, stop and fix them. Flaky tests have cost me many hours of my time in the past.

###  Actually sit with users and watch them work 

What _the business_ thinks the users needs vs what the user _actually_ needs is often very different. I have been lucky enough to witness this first hand where we saved ourselves a ton of work by actually watching a user at work and we were able to identify a very cheap and simple solution that they actually want vs the extremely costly solution the business proposed. 

###  User stories are a conversation starter 

If a user story prescribes exactly what software to write, who made that decision? Why? How did they know they were correct? 

This kind of approach of a "tech lead" or whatever deciding how to write the software creates disillusioned developer robots who have no sense of ownership and stories that are "blocked" because they have not been blessed by some over-controlling leader.

User stories should describe a user problem and when it is picked up the team figures out a way to do it and then they execute that plan, simple as that. This has a higher chance of success because more people are thinking about the problem and makes people feel involved.

Each ticket have some kind of measure of success that should be validated when enough data/research is gathered.

###  Understand that _we are all software developers_

In my imaginary company if you consider yourself a "backend" developer and consequently get blocked because the "frontend" developer is sick consider yourself fired. Same if the UX designer is away and you don't want to take a punt at how a particular interaction should pan out. 

You should have an appreciation of all aspects of software development. That's not to say you have to be an expert in everything but being blocked because a particular person is away is unacceptable. 

You should feel empowered enough to give whatever task a try. It doesn't matter if it's not perfect because it's better to ship something that is 70% good and then when the expert returns you can then **iterate** on the software to make it better.

When I said pairing earlier I didn't just mean "backend developers" or whatever. Everyone should be involved. If a UX designer is interviewing users it is their responsibility to bring along someone else to get experience of this skill and learn about the users. This kind of knowledge sharing is _vital_ to make individuals that feel invested in the project and the team. 

###  Have 10/20% time 

Allocate time for everyone to work on whatever they want and be strict about it. 

We work in a creative profession and we need some space to breathe, learn things and try out different ideas. 

This is a great perk for the team, can help avoid burnout and can help bring new ideas that can bring great improvements to your systems down the line. 

###  Don't plan extensively beyond 6 weeks 

Having a vision of the future is fun, but keep it a vague and aspirational. Remember a team focused on one or two features is far more productive than one which is worrying about 10 imaginary requirements.

###  No Jira, no estimates, no timekeeping, no burn-up charts 

All a massive waste of time, causes friction and I haven't seen a single burn-up chart in my career deliver any kind of _actual useful information_. 

Remember we have committed to showing _**real working software**_ frequently, **not imaginary charts** which are at best educated guesses. Finger in the air guesses are fine, adding up story points for tickets that have no hope of being actually looked at in the next 3 months is worthless.

> [Individuals and interactions over processes and tools](https://agilemanifesto.org/)

By all means have a simple, physical wall with the columns of ready for dev, in dev & done but much more than that it just becomes silly.

##  Wrapping up 

The way to move fast is not imagine the perfect product, architecture, design a backlog and then execute it. 

The way you move fast is by iterating quickly with low-effort, proven methodologies and communicating with each other as you learn through your iterations. 

Optimise your processes so that your team can fearlessly and quickly change software. This way you will be able to build a good product guided by constant feedback loops.

There is no one true way to create great teams who can ship great products but in my experience so far these principles seem to stand up well. Your way might be different and that's fine but ask yourself if your team is as good as it could be. Retrospection is always important to help your team adapt to new conditions. 
