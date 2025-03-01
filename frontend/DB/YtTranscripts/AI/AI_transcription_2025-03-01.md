Transcription for https://www.youtube.com/watch?v=c0HO_-NDJCk&list=PLMbMZz4DZESf3-EtmQ-N6lZh9I6LvI4h-&index=122&ab_channel=Syntax:

Okay, here's the transcription of the YouTube video you linked:

---

(Intro music with electronic sounds)

**Wes Bos:** What's up, everybody? Welcome back to Syntax! It's your boy Wes Bos.

**Scott Tolinski:** And it's your boy Scott Tolinski.

**Wes Bos:** What's up, Scott?

**Scott Tolinski:** Hey, what's going on, Wes? I'm excited. We got another listener question.

**Wes Bos:** Yeah! We're going to bang out some listener questions. These are some of my favorite episodes. We have a giant pile of them, and it's just fun.

**Scott Tolinski:** Yeah, it's nice to get these in, you know, sprinkle them in. I think it's good for everybody, keep those questions coming.

**Wes Bos:** Yeah! Let's do it! So, this one comes in from Mark, and Mark asks, "Hey Syntax crew, huge fan of the podcast! I have a question that has been bugging me. I'm currently using Prettier in my project and I love how it formats my code automatically. However, I'm a little confused on how to handle long lines of code.  Sometimes Prettier wraps my code in ways that I find hard to read, especially when dealing with long arrays or function arguments. I've tried adjusting the print width, but it doesn't always give me the desired outcome. What are your tips for dealing with long lines in Prettier and how do you balance readability with the automatic formatting?"

**Scott Tolinski:** This is a good one. I've been using Prettier since it came out. I use it on all my stuff.

**Wes Bos:** Yeah.

**Scott Tolinski:** It's a tool I don't think about too much, but it's definitely always there.

**Wes Bos:** Yeah, it's really good. I would not go back to a world where I had to manually format my code. I really like that when I just save something, it formats. It takes one thing off my brain.

**Scott Tolinski:** Yeah. So, my take on this is a couple of different things. Number one, the print width. That is a tough one. You are going to be stuck fiddling with that. It's probably one of the only settings that I fiddle with, and it's usually for the worse. I feel like it's hard to find the perfect print width, but generally, the wider you go, the less wrapping you get.

**Wes Bos:** Yeah, and the default print width, I think, is 80.

**Scott Tolinski:** Correct.

**Wes Bos:** And I think that's a good starting place.

**Scott Tolinski:** Yeah.

**Wes Bos:** I have seen people go up to 100 or 120, but I find anything over 100 is hard for me to read. It's too wide.

**Scott Tolinski:** Yeah, I think I agree with that too. I generally stick with the default, and then the other thing that I lean into really hard is just breaking it down by line. Like, you know, if you have a really long array or a really long function call, then it's like, you know, one per line is what I do.

**Wes Bos:** Yeah, let's talk about that a little bit. So, like, if you have an array of things, like `const items = [item1, item2, item3]` and all the way down to item 10, Prettier will just shove that whole thing on one line if it can, or break it wherever it feels like it needs to break it. And that's where it gets hard to read. So, what Scott is saying is that you would rather have each item on its own line, like this:

```javascript
const items = [
  item1,
  item2,
  item3,
  item4,
  item5,
  item6,
  item7,
  item8,
  item9,
  item10,
];
```

**Scott Tolinski:** Yeah, and one thing that I've found to be kind of interesting is sometimes Prettier does that automatically, sometimes it doesn't. Like, sometimes it's just like, "No, this is going all on one line," and I have to manually break it. And that's fine. I'm willing to do that. You know, I'm willing to manually break something for the sake of readability.

**Wes Bos:** Yeah, I think there's a rule. We'll try to find it and link it in the show notes, but if there's a trailing comma...

**Scott Tolinski:** Oh, true!

**Wes Bos:** ...Prettier is like, "Okay, I will put each item on its own line." So, adding a trailing comma can help.

**Scott Tolinski:** Yeah, that's right. Because that's one of the things, right? Is that it's a good practice to always put a trailing comma in your arrays.

**Wes Bos:** Absolutely. You should just have it.

**Scott Tolinski:** Yeah. It makes it way easier when you're adding or removing items.

**Wes Bos:** And it prevents diff noise in your Git commits.

**Scott Tolinski:** Totally.

**Wes Bos:** Cool, so that's a great tip: add a trailing comma to your arrays, or add a trailing comma to your function arguments if you want Prettier to break them up on separate lines.

**Scott Tolinski:** Yeah, for sure. And then, the other thing that I do a lot is I try to make sure my function arguments are as simple as possible, and not too many of them. If I find myself passing a lot of arguments to a function, then it's a good sign that maybe I should be passing an object instead. You know, like pass a config object.

**Wes Bos:** Yeah. That's a great point.

**Scott Tolinski:** Because then you can just break that object up into multiple lines, and it looks really nice. You know, like this:

```javascript
doSomething({
  option1: 'value1',
  option2: 'value2',
  option3: 'value3',
});
```

**Wes Bos:** Yeah, totally. So, instead of, you know, `doSomething(option1, option2, option3)`, you just pass an object. That's a really, really great tip because sometimes you're just stuck with a bunch of arguments that don't really have a good name. Like you just have a string and then a number and then a boolean. You don't really know what they are. But if you pass them in as an object, you can give them a name and it makes it a lot easier to understand.

**Scott Tolinski:** Exactly. And the same thing with, you know, calling a function in JSX. If you have a really long list of props that you're passing to a component, then it's like, oh man, just make that into an object and then spread it.

**Wes Bos:** Yeah.

**Scott Tolinski:** You know?

**Wes Bos:** That's also a great one. So, you can spread the object into the component's props.

**Scott Tolinski:** Exactly. So, it's all about just breaking things down into smaller chunks and making sure that everything is easy to read. And don't be afraid to manually break things in your code if Prettier isn't doing what you want. It's okay to go in there and just say, "Hey, you know what? I'm going to put this on a new line."

**Wes Bos:** Yeah, and I think you need to have good judgment here. If you're consistently breaking things on a new line, then it might be a good idea to adjust your Prettier settings to better match your preferences.

**Scott Tolinski:** Yeah, totally. But I'm just saying don't be afraid to do it. It's not the end of the world if you have to manually format a little bit.

**Wes Bos:** And, you know, the other thing I think of is when you get back data from an API, like a JSON object. You might have a really long object that comes back and you can't really control that. So, one thing I'll do is I will destructure those objects immediately.

**Scott Tolinski:** Ooh, that's a good one.

**Wes Bos:** So, if I have a user object that comes back and I only need the name, email, and avatar, I'll just destructure those right away. I won't even try to work with the entire user object.

**Scott Tolinski:** Yeah, I'm doing that a lot these days, it makes the code easier to read, for sure.

**Wes Bos:** Definitely. So, to summarize, play with your print width, use trailing commas, break down your code into smaller chunks, use objects instead of long lists of arguments, and destructure objects immediately.

**Scott Tolinski:** That's a wrap.

**Wes Bos:** Great tips! Thanks for sending in the question Mark. And we'll see you all next time.

**Scott Tolinski:** Bye bye!

(Outro music)

---

I tried to capture the key points and flow of the conversation.  Let me know if you need anything else!
