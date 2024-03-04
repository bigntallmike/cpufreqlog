=====================================
CPU frequency collection with rrdtool
=====================================

I wanted a way to track the frequency my CPU cores were running at over
time so as to more easily go back and see how it was performing,
especially with relation to heat and fan speeds.

This very small project is the result so far.  As of now, it simply
creates the RRD file necessary and updates the values once per second.

TODO
====

 * Create some common graph definitions 
 * Store temperature and fan speed data
 * Add configurability of intervals and data location