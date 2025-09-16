# automatic-content-generator

an automatic content generator that randomly selects user-provided search terms and finds excerpts from relevant youtube videos, ultimately splicing them together

more documentation to come

todo: create random 11 char long string that is then checked with the youtube api to see if it turns up as the video id for any videos

i found that the current implementation of youtube search consistently pulls up the same "random" videos. I need to reimplement my random searching code to make it truly random. the randomized 11 char string is a way to do that.
