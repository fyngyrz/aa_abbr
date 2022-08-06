# README.md

## Overview

Often when writing for the web, we lean into using abbreviations. <abbr title="Random Access Memory">RAM</abbr>, 
ROM, <abbr title="HyperText Markup Language">HTML</abbr>, <abbr title="Red Green and Blue">RGB</abbr>, <abbr title="In Other Words">IOW</abbr>, <abbr title="Miles Per Hour">MPH</abbr>, and so on. Sometimes it's reasonable to expect
your readers to know what they mean... but surprisingly often the things
we take for granted as known... aren't. This project is specifically
intended to help address that in a comfortable way without changing your
writing style much (all you have to keep in mind is that terms you want
definitions to appear for need to be surrounded by spaces), or even your
presumptions about your readers.

This `Python3` class, `aa_abbr.py`, takes <abbr title="HyperText Markup Language">HTML</abbr> text as input, and using a
terms definition file, generates <abbr title="HyperText Markup Language">HTML</abbr> `<abbr>` tags to wrap the terms you
have defined.

In the provided definitions file, the term <abbr title="Random Access Memory">RAM</abbr> is defined this way:

> `RAM,Random Access Memory`

This is what it looks like (in the Chrome browser) when a visitor to the
 <abbr title="HyperText Markup Language">HTML</abbr> page hovers their mouse over the term <abbr title="Random Access Memory">RAM</abbr>: 

> ![aa_abbr\(\)](example.png)

## Usage

Basic use is very easy:

```Python
import abbr from aa_abbr    # import class
ab = abbr('abbrdefs.data')  # instantiate class
outText = ab.abbr(inText)   # use class
```

In addition, there are `set` calls that provide comprehensive control of
class behavior, as well as `get` calls that read back the class's current
states. These are listed at the top of the class in the comments.

One useful function is the ability to set a list of terms to be ignored,
even though they are present in the definitions file. You can do this at
instantiation, or by calling...

> `setNopelist(['term1','term2','termN])`

...you would do this when a term is used in an unusual way that calls for
it to be ignored in that particular context.

Another way to do this dynamically is to surround a term you don't want
processed with <abbr title="HyperText Markup Language">HTML</abbr> space entities instead of actual spaces: `&#32;` That
will prevent that particular instance of the term from being processed by
`abbr()`.

## Data File

The defaults for the definitions file are:

* Blank lines are ignored
* Lines beginning with `#` are ignored
* The first comma delineates the term from the definition(s)
* A pair of vertical bars (`||`) delineate multiple definitions

When there are multiple definitions, they will be numbered. This is what
that looks like:

### In the definitions file:

> `R/C,Remote Control||Radio Control`

### In your source code:

> &quot;<tt>&nbsp;<tt>R/C&nbsp;drone, hover</tt>&quot;

### In the browser:

> ![aa_abbr\(\)](drone.png)

You can set which characters in the definitions file do what. The only
hard-coded behavior in terms of reading the definitions file is ignoring
blank lines.

You can change these things either when invoking the class, or using
various `set` calls within the class prior to calling the processor. You
can also change which definitions file you use any time prior to
processing the text.

When defining terms in the definitions file, be aware that most <abbr title="HyperText Markup Language">HTML</abbr> is
not allowed other than <abbr title="HyperText Markup Language">HTML</abbr> character entities. This is partially because
the hover text in an &lt;abbr&gt; tag is contained within double quotes,
like so...

> `<abbr title="Random Access Memory">RAM</abbr>`

...and partially because hover text is not parsed by browsers for <abbr title="HyperText Markup Language">HTML</abbr> 
formatting information.

You can use double quotes in a definition but you must encode them as
their <abbr title="HyperText Markup Language">HTML</abbr> entities:

> `&quot;`

The provided definitions file `abbrdefs.data` contains a variety of
commonly used terms. You should expand it to include any other terms you
desire. Adding terms will not slow down the processing step. A longer
definitions file does linearly increase the instantiation time, but
generally speaking, this should not be significant.

## Efficient Use

The class reads the definitions file once when it is instantiated. It
won't read it again unless you call...

> `setSource('definitionsFILEname')`

...to change or re-read it.

When processing your <abbr title="HyperText Markup Language">HTML</abbr>, each word delineated by leading and trailing
spaces or a leading space and a trailing _single_ non-alpha-numeric
character prior to a trailing space is processed. So <abbr title="Random Access Memory">RAM</abbr> would be
processed here:

> &quot;<tt>&nbsp;RAM.&nbsp;</tt>&quot;

But _not_ here:

> &quot;<tt>&nbsp;RAM.&lt;p&gt;</tt>&quot;

You can easily compensate for this by surrounding the `<p>` tag (or any
other tag) with spaces, which the browser will collapse (hide) in the
context of typical whitespace processing:

> &quot;<tt>&nbsp;RAM.&nbsp;&lt;p&gt;&nbsp;</tt>&quot;

A similar issue exists at the beginning and end of lines. If a term
starts a line, the preceeding character was an <abbr title="End Of Line">EOL</abbr> character rather than a
space, so the term won't be caught. Simply add a space at the beginning
of the line in the text to resolve this. Again, the browser will collapse
the additional whitespace.

`abbr()` will catch plurals by default, that is, terms that have a
trailing `s`. So if `ROM` is defined in the terms file, both <abbr title="Read Only Memory">ROM</abbr> and <abbr title="Read Only Memory">ROM</abbr>s 
will be processed. You can disable this behavior at instantiation or by
calling `setPlurals(False)`.

If the plural term is located at the end of a line, the presence of the
terminating `s` followed by the <abbr title="End Of Line">EOL</abbr> character is seen as _two_ non-alpha
characters, and the term will not be processed. Again, just add an extra space
after the term to resolve this.

When plural detection is on, text processing is a little slower. This has
not been a problem for me, but <abbr title="Your Milage May Vary">YMMV</abbr>. 

## A <abbr title="Cascading Style Sheet">CSS</abbr> tip

The following <abbr title="Cascading Style Sheet">CSS</abbr> adds a red, dashed underline border to an `<abbr>`
tagged term:

> <tt>abbr {border-bottom: red dashed;}</tt>

Like this:

> &quot;<tt>The <span style="border-bottom: red dashed;"><abbr title="Read Only Memory">ROM</abbr></span>&nbsp;</tt>chips&quot;

## Somewhat Subtle Gotchas

When you have <abbr title="HyperText Markup Language">HTML</abbr> in your file, there are some <abbr title="HyperText Markup Language">HTML</abbr> tags that have what
amounts to raw text in them. For instance, the `<img>` tag can contain
`title="some title text"`. If a term appears surrounded by spaces inside
those quotes, and `<abbr>` tags will be generated _inside_ the title
quotes. Browser confusion can result.

To avoid this, you can use space entities instead of actual spaces around
the term(s) at issue:

> `title="some&#32;ROM&#32;code"` 
