title: 실용 행사 안내서
source: https://opensourceevents.github.io/ 

# 실용 행사 안내서

## 자신의 오픈소스 프로젝트에 새로운 기여자를 맞이할 준비하기

요즘은 오픈소스 프로젝트에 새로운 기여자를 초대하기 위한 여러 워크샵, 해커톤, 스프린트 같은 것들이 매일 열리는 것 같습니다. [OpenHatch](http://openhatch.org/)에서도 이런 행사를 많이 열고 있습니다! 이런 행사에서 최대한 잘 이끌어내기 위해서는, 무엇보다 잘 준비하는 것이 중요합니다. 목표를 설명하고, 적절한 작업을 선별하며, 프로젝트 설정을 테스트하는 것 모두 한 발짝 나아가고 좋은 시간을 보내는 데 중요합니다. 이러한 변화 덕분에 더 나은 경험을 제공할 수 있었기 때문에, 이런 일들은 (분명히) 해볼만 한 가치가 있다고 생각합니다.

그래서 우리는 오픈소스 프로젝트의 행사 개최를 돕기 위한 다음 안내서를 만들었습니다. 아래 예제에서 보듯 저희 프로젝트 - [OpenHatch.org](http://openhatch.org/) 웹 앱 - 에 사용했던 것입니다. 마지막 부분에 체크 리스트도 준비해 두었습니다. 이 안내서에 나온 내용을 요약하고 있어 행사를 준비하며 진행 상황을 점검할 때 활용할 수 있을 겁니다.

이 안내서 또한 [오픈소스](http://creativecommons.org/licenses/by/3.0/us/) 입니다. 여러 기여자 분들에게 감사드립니다. ([당신도 기여할 수 있습니다!](https://github.com/openhatch/in-person-event-handbook))

### 목표를 정의하기

You want to be able to state clearly your goals for the event, as this gives your group something to work towards. You can start by asking:

#### 당신의 프로젝트의 종합적인 목표는 무엇일까요?

You want a short (1 paragraph or less) answer to this question which you can use to entice potential contributors to your project. Details are great, but at this point, you shouldn’t need to be too technical. At many events, such as the PyCon sprints, you'll be asked to give a short summary in front of everyone. Why not be prepared?

> OpenHatch’s goal is to make the free software/open source community more welcoming to newcomers. To do this, we provide curricula and logistical support for running “Intro to Open Source” workshops, a website with open source tools, “training missions” and a volunteer opportunity finder, and several other projects in progress.

#### 이 행사를 통해 어떤 것을 달성할 수 있을까요?

Think about what, specifically, you’d like to get done at this event. You can break these down by elements of your project, if you have more than one. It should be clear how these event goals contribute to the overall goal of your project. At the same time, these are not “tasks” - it should be necessary to break these goals down further in order to accomplish them.

It’s useful to phrase these in terms of “Base” and “Stretch” goals. Having modest base goals gives you something to celebrate at the end of the event, while adding stretch goals lets you plan for the exciting scenario of having a large and/or effective team that’s able to accomplish a ton.

In general, it’s better to have too many goals than too few, but make sure you prioritize them. When you get to the task-breakdown part of this guide, focus on doing a thorough job with each individual goal before moving on to the next one.

  * Make a new training mission
    * Base goal: Pick a skill to create a new training mission around, and design what the mission will look like. Create a mock-up of the mission.
    * Stretch goal: Implement the mock-up, and user test it on volunteers from the event.
  * Clean out issue tracker
    * Base goal: Go through tracker and label issues by what type of “cleaning” they need. Does a bug need to be verified? Does a patch need to be tested? Does the feature request need to be attached to a milestone?
    * Stretch goal: Use the labels as a guide to "clean" each issue. Verify bugs, test patches, etc.



### 프로젝트 설정하기

In our experience, project setup is the single biggest barrier to participation. We’ve seen (and run!) events where participants spent most of their time just getting their development environment set up and becoming acquainted with the project. If your goal is for newcomers to make contributions, estimate how long you think it will take them to set your project up. Then find a friend or two who's not familiar with your project to test and see how long it _really_ takes. You can also find someone to help you do this in [#openhatch](http://openhatch.readthedocs.org/en/latest/contributor/chat_on_irc.html).

Documenting and improving the process beforehand can save everyone a lot of time and energy. If you know that a part of your project will inevitably be time-consuming, make sure participants know to expect that.

All of the information below should be documented in a README at the top level of your source repository. Other places to put the info include a “Want to contribute?” section of your project website, and/or you can include a link to the README in the signature of your mailing list or in the status bar of your IRC channel.

#### 프로젝트 커뮤니티와 관리자는 어떻게 찾을 수 있을까요?

Contact information should be displayed prominently, as you may have remote contributors, or contributors who want to start before the event. Types of contact information can include:

  * A link to your mailing list.
  * Your IRC channel name and server (including link to IRC installation guide and link to webchat version).
  * Social media accounts such as Identica, Twitter, Facebook, if your project has them.
  * Maintainers’ personal contact information, if you feel comfortable giving it out.



If you have a preferred mode of contact, do specify.

> OpenHatch has two places for contact info, which we try to keep updated and consistent with each other. There’s our [contact info in the documentation](http://openhatch.readthedocs.org/en/latest/community/contact.html), primarily linked to from our source code repository, and our [contact info in the wiki](https://openhatch.org/wiki/Contact), primarily linked to from the website’s main page.

#### 프로젝트의 구조

Describe the basic structure of your project. What are the biggest pieces and where are they located? How do those pieces interact? Then break each piece down. You don’t need to talk about every file or subdirectory of your project, but you don’t want to assume that what a script does, or how the files in a directory interact, or what language a part of your project is in is obvious to a newcomer. Making those assumptions turns getting access to you into the bottleneck resource for working on your project.

Depending on the size and complexity of your project, this can be a pretty big undertaking. At OpenHatch, we’re still working on getting the full structure completely documented. We recommend doing a “top level” explanation of your project’s structure - enough detail to fill a half a page to a page. When you have more time, you can go into more detail, starting with the areas that people commonly work on (or are likely to work on at sprints or hackathons.) If you use other frameworks or libraries, you can save yourself some time by linking to their documentation and tutorials.

> A description of the top-level structure of the OpenHatch project can be found at [Project Overview](http://openhatch.readthedocs.org/en/latest/getting_started/project_overview.html). A description of the structure of OH-Mainline (the repository that runs our website) can be found [here](https://github.com/openhatch/oh-mainline/blob/master/LAYOUT).

#### 자신의 작업 환경 설정하기

In order to contribute to your project, people will usually need to set up a local version of the project where they can make and test changes. The more detailed and clearer your installation/development guide, the better.

Here are common elements of setting up a development environment you’ll want your guide to address:

  * Preparing their computer
    * Make sure they’re familiar with their operating system’s tools, such as the terminal/command prompt. You can do this by linking to a tutorial and asking contributors to make sure they understand it. There are usually great tutorials already out there - OpenHatch's command line tutorial can be found [here](https://openhatch.org/wiki/Open_Source_Comes_to_Campus/Curriculum/Laptop_setup#Goal_.232:_practice_navigating_from_the_command_line).
    * If contributors need to set up a virtual environment, access a virtual machine, or download a specific development kit, give them instructions on how to do so.
    * List any dependencies needed to run your project, and how to install them. If there are good installation guides for those dependencies, link to them.
  * Downloading the source
    * Give detailed instructions on how to download the source of the project, including common missteps or obstacles.
    * If there are multiple versions of the project, make clear which version they should download.
  * How to view/test changes
    * Give instructions on how to view and test the changes they’ve made. This may vary depending on what they’ve changed, but do your best to cover common changes. This can be as simple as viewing an html document in a browser, but may be more complicated.



Installation will often differ depending on the operating system of the contributor. You will probably need to create separate instructions in various parts of your guide for Windows, Mac and Linux users. If you only want to support development on a single operating system, make sure that is clear to users, ideally in the top-level documentation.

> You can see OpenHatch’s version of this information in our [Installation Guide](http://openhatch.readthedocs.org/en/latest/getting_started/installation.html). General instructions for testing changes can be found [here](http://openhatch.readthedocs.org/en/latest/getting_started/handling_patches.html#test-your-changes). Specific tasks may have additional documentation (for instance, [documentation changes](http://openhatch.readthedocs.org/en/latest/getting_started/documentation.html).)

#### 변경 사항을 제출하고 의견 주고 받기

How do contributors contribute their changes to the project? Do they submit a pull request via Github? Do they generate a patch and attach it to an issue in an issue tracker? Make sure this information is explicitly provided.

> OpenHatch’s guide to submitting changes can be found [here](http://openhatch.readthedocs.org/en/latest/getting_started/handling_patches.html).

It’s also useful for people to know how they can give feedback/report bugs to the project. If your project doesn’t have an issue tracker, consider creating one. On Github, all repositories come with issue trackers (though you may need to enable it by going to _Settings_ and then _Features_.) There are many other [issue tracking systems](http://en.wikipedia.org/wiki/Comparison_of_issue_tracking_systems).

If your project is small, you may not want or need an issue tracking system. That's fine. What's key is that contributors know how to give you feedback.

> Issues with the Open Source Comes to Campus project can be reported [here](https://github.com/openhatch/open-source-comes-to-campus/issues?direction=desc&sort=created&state=open). Most other issues with OpenHatch can be reported [here](http://openhatch.org/bugs/).

Tools like issue trackers are very useful for asynchronous communication. This may not be the best fit for an in person event. If you want to change things up - for instance, by having attendees ping you in IRC with links to new issue URLs, so they don't fall between the cracks - make sure to tell them that!

#### 문서화 확인하기

Verify that this documentation is complete/effective by testing on individuals who haven’t used or contributed to your project before. Find at least one person for each operating system to read your documentation and attempt to install, make and test changes, and contribute the changes to the project. (These can be simple, fake changes or, if your tester is willing, actual tasks.) Make sure your testers have similar skills/experience as the kinds of newcomers you expect to have at your event.

If you're having trouble finding people to help, try the [#openhatch IRC channel](http://openhatch.readthedocs.org/en/latest/contributor/chat_on_irc.html).

Make sure that any problems which arise during verification are added to the documentation. Once the documentation has been verified, and a line to the top of your guide which states what was verified and when.

> Development environment instructions tested successfully on Ubuntu 12.04 (on 2013-10-03), Mac OS X 10.8 (on 2013-10-01) and Windows XP (in Jan 2005). You can see OpenHatch’s version of this [here](http://openhatch.readthedocs.org/en/latest/getting_started/installation.html).

Ideally, you should verify that installing, making and testing changes, and contributing changes all work. If you only have time for one, we recommend verifying installation. In our experience, that's where the majority of problems arise.

### 참가자를 위해 일감 정의하기

Let’s return to the event goals we talked about in the first section. Each goal should be broken down into the discrete steps needed to reach it. These steps are the tasks you give to participants.

These tasks should include a “plain english” summary as well as information about where to make the changes (for instance, which files or functions to alter). We recommend including a list of needed skills (e.g. “design skills”, “basic Python”) and tools (e.g. “Mac development environment”). It’s also useful to include an estimate of how much time the task will take, to label some tasks as higher or lower priority, and to mark where one task is dependent on another.

This may seem like a lot of work, but it should help your attendees quickly and easily find tasks that are suited for them. Since one of the main goals of in-person events is to give attendees a positive experience, we think it's worth it.

#### 일감을 관리하는 시스템을 만드세요

We recommend using a wiki or similar planning document to keep track of tasks. OpenHatch has [a task browser](https://github.com/openhatch/new-mini-tasks) that we use for our events - you are welcome to fork it and customize it for your project/event, although you might want to wait as we’ll be making some big improvements soon. Something as simple as an etherpad should also be just fine. (See [here](https://etherpad.mozilla.org/task-browser-template) for a template and a service you can use.)

#### 일감 준비하기

To figure out how many tasks to prepare, we recommend using the length of the event and the number of expected participants to predict how many person-hours will be spent working on your project. You can then use the time estimates you made for each task to see where you stand. We suggest finding 30% more than you think you'll need, as it's better to have too much to do than too little.

  * Base goal: Go through tracker and label issues by what type of “cleaning” they need. Does a bug need to be verified? Does a patch need to be tested? Does the feature request need to be attached to a milestone?
    * Task 1: Label issues
      * Skills/tools needed: Moderate English language skills, familiarity with concepts of verification, testing, milestones.
      * Estimated time: ~20 minutes per issue
      * Get started: Familiarize yourself with the issue tracker and how it displays information. (See this documentation.) Request administrative access so you can add labels to the tracker.
      * For each issue: Read the thread for each issue and identify where in the process of addressing the issue the community is. If there is an unverified bug, add the label "Unverified". If there is an untested patch, add the label "Untested patch". If there's a feature request with no associated milestone, add the label "Needs milestone".
  * Stretch goal: Use the labels as a guide to "clean" each issue. Verify bugs, test patches, etc.
    * Task 1: Verify Bugs
      * Skills/tools needed: Moderate English language skills, ideally familiarity with virtual machines to test on multiple OSs.
      * Estimated time: ~15 minutes set up, ~20 minutes per bug (high variance)
      * Get started: Download the development environment and make sure you can run the project. Make sure you have an account on <the issue tracker> and are familiar with how to add comments or change labels.
      * For each bug: Try to reproduce the bug. Record the results in a comment, including your operating system type and version #. If possible, test on multiple browsers. If there are recent comments covering all three major OSs, add label to bug “ready_for_maintainer_review”.



No matter what, attendees will need to be matched to a task that fits their skills and interests. Doing this prep work will let participants get started immediately, instead of making them wait for you to suggest an appropriate task. Ideally, event organizers will have collected information on participants' skills and interests ahead of time, so you can tailor the task list to your group of contributors.

Making the steps of each task explicit also helps participants mentor each other. By clearly identifying which skills and concepts are needed, you make it easier for individuals to say, "Oh, I understand how to do that! Let me show you."

### 그 다음엔,

Contributors may not be able to finish the tasks they are working on during the event, or they may want to continue participating in the project by working on other tasks. Thinking ahead about how you will follow up on the event makes it easier to exchange information with participants and plan the direction of your project.

We recommend asking each participant to answer the following questions about the tasks they worked on. Giving them this list at the start of the event will help them document what they’re doing as they go along. You can print out the list, email it to attendees, make a web form - whatever suits you.

  * For each task you worked on, please answer:
    * What task did you work on?
    * Please briefly document your workflow. What steps did you take, in what order, and why?
    * Where can I find the work you did at the event? This includes code, documentation, mock ups, and other materials.
    * If you created any accounts for the project, please list the site and account name. Make sure to store the password in your favorite password manager, or make sure I (or another maintainer) knows it.
    * What obstacles did you encounter when working on this task? Do you have any feedback for me to make the process better for future contributors?
    * Would you like to stay involved in this project? If so, in what capacity?



If there is enthusiasm for continuing the work, make sure you stay in touch! We suggest gathering emails from interested attendees and contacting them within 48 hours of the event. In the email, thank them for their help and include information on how to stay part of the community via, for instance, IRC or mailing lists.

We also recommend planning a follow up meeting at the event. If you’re all local, try setting a date after the event for you and your team to meet at a local coffee shop, coworking space, or project night. If you’re remote, set a date to meet on IRC or a google hangout. 2-3 weeks is a good time frame, though it will depend on how busy you and your new contributors are.

### 체크리스트

That’s a lot of advice! To help you keep track of each step, we’ve created two checklists for you. The detailed version includes all of the advice above. The quick and dirty checklist includes the elements of the above document which we think are most important. We recommend starting with the quick and dirty checklist. Once you've completed that successfully, you can go back and do the extra steps if you have the time and energy.

To view and/or print the checklists, go [here](https://github.com/openhatch/in-person-event-handbook/blob/master/checklists.pdf).

### 알림

Thank you to everyone who has contributed to, or helped inspire, this project.

#### 기여자

  * Shauna Gordon-McKeon: maintainer, content
  * Ni Mu: design
  * Sheila Miguez: content feedback
  * Asheesh Laroia: content feedback

#### 더 알아보기

  * [Open Advice](http://open-advice.org/)
  * [Producing Open Source Software](http://producingoss.com/en/producingoss.html)
