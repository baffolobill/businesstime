businesstime
============

This fork was completelly rewritten. It based on this https://github.com/florianv/business PHP project. So, if something doesn't work, just ensure that I didn't make mistake when porting it to Python. From the entire project I actually need only one method - `Business.timdelta`, which calculates a business time, spent to solve some task.

Unfortunatelly, there is not tests yet. Just awful `businesstime/test_1.py` with prints and comments.
Also it doesn't handle properly the case when some tasks starts/ends before/between/after inverval(s). What I'm trying to say. Let's look at this picture:

    +-------------------------------------+
    |  (1)            (2)                 |
    | --*--|--------|--*--|--------|--    |
    |      9       13     14       18     |
    +-------------------------------------+

At point (1) employee starts to work on some task (for instance, in 8:30 a.m.). At point (2) - he finished (for instance, in 13:20). `Business.timedelta` takes into account only time from 9 to 13. It meens, our employee solved the task for 4 hours. But it is not. He completed it in 4 hours and 50 minutes.

Described above case is very simple and it will be solved in nearest future. But there are others:
1) employee has a break between 13 and 14 o'clock. He didn't notice that it's time for a break and started work on a task at 13:01. Should we consider this as a job during the break?
2) the same problem happens when a task started after the end of a work day. If the task will be finished in the same day, we just do difference between this values. But what if it will be finished at 8:30 in the next day?


Features
--------

- Using intervals to define working hours
- Supports holidays
- Calculates timedelta


UnFeatures
----------

- Has no normal tests
- Does not support timezones
- Has unsolved cases, when a task start/end time lies before/between/after defined intervals
