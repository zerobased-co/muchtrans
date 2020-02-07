title: How NOT to hire a software engineer
author: Nikita
source: https://tonsky.me/blog/hiring/
link_hreflang: en
link_title: en_US

# How NOT to hire a software engineer

I’m not an expert in hiring for big companies, but I have extensive experience for small ones and a bit of common sense.

Back in 2013, I ran a highly successful hiring campaign for [AboutEcho.com](https://web.archive.org/web/20140101000655/http://aboutecho.com/) that led to the hiring of nine senior-level engineers. My Russian-speaking readers could [read about it here](https://tonsky.livejournal.com/288899.html).

All that gives me the confidence to criticize practices Internet Giants use to hire engineers to this day.

## Don’t aim for the best solution

When you arrive at the interview, the interviewer gives you a problem and expects a solution in zero to two minutes. If you spend longer they really start to worry and ask to go with at least something.

I can understand that—after all, they only have 45 minutes and there are lots of things they want to go through with you.

What I can’t understand is that you’re judged by the quality of the solution you came up within two minutes. Because that’s not how human creativity works. It’s easy to come up with many ideas, but strange to expect that best one will always be first. Even geniuses can’t predictably generate world-best answers on a clock.

What creativity is is the ability to evaluate and filter the stream of ideas that you come up with. If you are really interested in that, why don’t you ask the interviewee to compare and evaluate multiple ideas? Check if the person can assess the properties of the proposed solution? If she clearly sees all the pros and cons?

And if you are asking to come up with the best possible solution in two minutes, what you are testing for is luck, nothing more. Are you in a business of hiring lucky employees? Or capable ones?

## Don’t ask puzzles

How to check if a linked list has a loop? Does one N-dimensional box fit into another N-dimensional box? Can you swap two variables without a third one? How to find the shortest distance between two moving ships? Find all permutations of N elements doing only N-1 swaps?

Those puzzles are fun to talk about and solutions to them can be very insightful. I used to enjoy lots of them reading [Mathematical Recreations and Essays](http://www.gutenberg.org/ebooks/26839) as a kid. Don’t take me wrong, they _are_ fun.

However, no matter how fun they are, they are merely anecdotes. The property of a puzzle is that you either know the answer to it or you don’t. It doesn’t tell you anything else. It has nothing to do with future performance, being smart, capable or anything else whatsoever. Knowing a particular answer does not mean you have an apparatus to solve real problems in a generic and predictable way. The only thing it tells you is that the person has been in a situation when someone shared a solution with him. Nothing more, nothing less. Just stop already.

![](https://tonsky.me/blog/hiring/puzzle@2x.png) How do you save yourself before candle burns the rope?

## Be open for alternatives

This is kind of expected, but big companies seem to still fail at this. If the interviewee proposes an alternative solution, it’s a chance for you as an interviewer to learn something. It’s also a good chance for an in-depth discussion if the proposed solution turned out to be impossible or bad somehow.

Still, I’ve been dismissed for proposing an alternative solution of the same complexity once (and burdened with a lecture on a “one true way to approach that problem”) and strictly led to a particular solution another time. In the latter the interviewer was very eager to ignore all my concerns and only wanted to discuss what he saw as a solution for a problem, later leaving “not impressed” feedback about me.

Nobody knows everything. Be open. Listen. Think. Yes, even if you are interviewing someone.

## Be tolerant for imperfections

Off-by-one errors are widely-accepted as one of the hardest problems in CS for a reason—everyone makes them. Errors are part of programmer’s life, not something you can get rid of. Good programmer simply knows what to do about it. Quality of a programmer is NOT defined by how few errors she makes.

Now, if you only select people who made no mistakes during the interview you won’t magically get a squad of programmers who always write perfect code. You just don’t know how they will behave when they will—inevitably—make their mistakes.

So mistakes are actually good because you get to learn how that person mitigates them. Don’t judge the errors, judge how interviewee handles them:

  * simple code,
  * divide and conquer,
  * self-checks,
  * invariants,
  * asserts,
  * compiling and running,
  * testing.



Oh, sorry about the last two. I forgot you don’t let them run their programs. Well, what did you expect then?

## Let me test!

Seriously, what’s the thing with writing program on a whiteboard?

I mean, I’m happy to discuss algorithms there—discussing abstract things is more efficient that way.

But writing programs, actual programs, in a notepad? Without even running them? What’s the point? Getting the first draft of the code is barely one-tenth of the whole process, followed by compiling, checking, tuning, testing, reviewing etc. Who are we kidding? Those are the essential parts of any coder’s workflow. A code is only good to look at when it’s past all those, not before.

It’s like asking a painter to do a painting of a horse, then stop her halfway during the very first sketch just when you can see four vertical lines for legs and judge that. How much will you learn about her?

![](https://tonsky.me/blog/hiring/horse.png)

## Get deep

Five short interviews? Or two long ones?

With five you get five independent opinions, which is better than two. But how deep can you get in 45 minutes? Practice shows it’s barely enough to write 20-30 lines of code and ask a couple of really simple questions (what’s the complexity? how you test it?).

The next interviewer simply repeats the same process, getting as far as the previous one. Which is not far. Not far at all.

Why not make it two, but make them really thorough? E.g. one before lunch and one after? Three hours is not much either, but at least you get the chance to see how person tests the code, how she changes it, how she works with requirements—all within an already established context, not resetting and starting from scratch every 45 minutes.

With that much time you can even ask her to write the code as if it is a part of a system, not just an abstract algorithmic task in a vacuum—and learn another thing or two about her real-world performance.

And if you want more opinions? Put multiple interviewers in the room and let them argue afterward.

## Learn the background

I mean, I have [fourteen years of experience](https://tonsky.me/projects/). I’d be happy to talk about functional programming, distributed systems, consensus, replication, collaborative text editing, CRDTs, parallel architectures, UI frameworks, team processes, product design, user experience. I have practical and research experience in all those areas. All of them are in direct interest for more or less any internet giants I’ve been interviewed at.

Was I ever asked about any of those? No.

What I get is “imagine you have a function that takes a list…” five times in a row. Five school-level problems are supposed to give you an adequate impression of what? How thorough was I reading Cormen et al? To be fair, you are rarely asked about those either.

Instead, fine-tune the interview for a candidate’s experience. Talk about what she is good at. You’ll get a chance to ask deep questions and learn a lot more about the experience level and the benefits she would bring to your company.

## Make the process seamless

Wrong directions? Delayed tickets? A questionnaire that requires installing the original Adobe Reader specifically? Cheap ultrabook with unfamiliar keyboard layout and poor web-based editor with no shortcuts whatsoever that lags even on a local machine? Excuse me, I am in the office of the most capable IT-company in the world, am I not?

In my case, the single recruiter was arranging five interviews a day. Five people every day. Times number of recruiters in that company. Imagine all of those candidates slightly frustrated by the process. Every day. Year after year.

You might think it doesn’t matter. Well, it depends. There was an episode of TV show Louie, where a comic’s name was misspelled on his door. So he argued: yes, it’s an easy mistake to make, but it’s also an easy mistake to fix. It doesn’t matter it’s just for one day, if you bothered at all, please do it right.

Yes, I believe anyone can do better.

![](https://tonsky.me/blog/hiring/recruiters.png)
How many recruiters does an IT campus fit?

## In closing

If you are in a business of hiring software engineers, big companies’ practices are not your friends. Common sense, fairness, tolerance, real interest, and open-mindedness are.

Good hiring!

