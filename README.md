pyLightWorks
============

Python powered controller that utilizes MIDI inputs to syncronize Rock Band light displays. Utilizing averaged time difference between midi inputs over a particular amount of notes hit, a rough level of song tempo and energy can be obtained. 

This performance data is the passed to the lightworks function which will then create a lightshow matching the song. 

Future versions will utilize averaged velocity of notes hit and ideally implement special events based off of unique number of notes hit in a narrow time range, potentially signaling a difficult track or drum solo. 
