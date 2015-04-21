# message-parser

### Summary

The Message class accepts a string representing a chat message and extracts
interesting information from it.

### How to run

```
git clone https://github.com/andrewtchin/message-parser.git
cd message-parser
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
python message.py
```

Enter the message string to parse at the prompt.

### Unittests

Run unittests:
```
nosetests
```

### Extracting message attributes

The message is searched based on a regex that defines the
attributes that we want to extract. This provides a performance
advantage over repeated searching of the tokenized strings for the
delimiting characters of interesting tokens.

To modify the attributes we search for, add a regex group
that matches the tokenized attribute.

### Specifications

* Accept chat message string.
* Mentions - start with '@' and end with non-alphanumeric character.
* Emoticons - 1 to 15 alphanumeric characters enclosed by parenthesis.
* Links - URL and page title.
* Output JSON of interesting message contents.

### Assumptions

* Message string will be truncated to max length of 1000000 bytes.
* Mention token must begin with '@'.
* Link token must begin with http:// or https://.
* No upper bound on length of username, subject to max message length.
* URLs are HTTP(S) because retrieving titles for other protocols would
not be relevant.
* Input validation is handled by the regex that specifies the attributes
we are interested in and will ignore any tokens that do not match.

### Limitations

* URL regex will only match HTTP(S) URLs. I used a simple regex, but the
regex could be improved to match other protocols or cases.
* Does not handle matching attributes that span multiple tokens.
* Does not handle matching multiple emoticons within a single token. Matches the
last emoticon within the token.
* Does not handle matching emoticon and mention in a single token. Matches the
first attribute within the token.

### Scaling

For larger messages or higher volumes of messages, multiprocessing could be used.
Message strings or partial message strings of large messages can be queued with
a message ID and number of parts.
A process pool can pull from the shared queue, map all the interesting tokens,
and push the result to a result queue. When all results for a given message ID
are complete, results are merged into the final result dict for the message and
returned.

### Sources

https://rushi.wordpress.com/2008/04/14/simple-regex-for-matching-urls/
https://daringfireball.net/2010/07/improved_regex_for_matching_urls
http://stackoverflow.com/questions/51233/how-can-i-retrieve-the-page-title-of-a-webpage-using-python
