# Lamarck_DNA
## Digital DNA and Lamarckian Evolution
This repository is intented to provide an open source proof of concept that artificial systems for DNA storage can be ‘Lamarckian’ in nature, where both forward and reverse flow of information can take place between genotype and phenotype. In our prototype, synthetic DNA is the genotype and sound is the phenotype. The system can capture both genotypic and phenotypic changes that can result from errors introduced in the read-write steps. Developed and tested with Python v3.6.13. 

---
## Table of contents

- [The Digital DNA system](#the-digital-dna-system)
    - [Encoding](#encoding)
    - [Decoding](#decoding)
- [Testing Lamarckian inheritance](#testing-lamarckian-inheritance)
	- [Synonymous mutation-workflow](#synonymous-mutation-workflow)
	- [Random-single point mutation-workflow](#random-single-point-mutation-workflow)
	- [Non-synonymous mutation at sound and DNA levels-workflow](#non-synonymous-mutation-workflow)
	- [Comparing audio files](#comparing-audio-files)
- [Running the codebase](#running-the-codebase)
- [Dependencies](#dependencies)
- [Helper scripts](#helper-scripts) 
	- [Generating MIDI file from music-score](#generating-midi-file-from-music-score)
	- [Generating music-score from MIDI file](#generating-music-score-from-midi-file)
	- [MIDI file correction](#midi-file-correction)
	- [Splitting MIDI file with multiple tracks](#splitting-midi-file-with-multiple-tracks) 
	
## The Digital DNA system
* The digital DNA system is formulated using an artificial 4-letter genetic code, which includes 256 possible permutations or combinations, of four-letter nucleotide sequences made from the four nucleotides (A,G,C and T)
* In our system, a codon represents a 4-letter combination which denotes a particular musical element (A musical element stands for a particular musical note with a specific pitch depending on which octave it belongs to, and specific note-length denoting the duration that a note is played)
* In the same way as the genetic code degeneracy works, here the 256 codons code for 64 unique musical elements, with four fold redundancy. (Hence, each musical element corresponds to a 4-letter codon, and there are four such 4-letter codons that can code a single musical element.)

The system performs the following steps:
### Encoding
> A simple musical score is coded as a DNA sequence. The code accepts a MIDI file as the input and maps each musical element to corresponding 4-letter codon to create the DNA sequence.
 
 Command syntax to encode DNA directly from a MIDI file
```
python3 main.py generate-dna -in <input-MIDI-file> -tempo <beats per minute>
```

 Parameters

>`in`: The input MIDI file ( a single track, 4/4 time signature MIDI). "-in" parameter input file should be kept in the 'Lamarck_DNA/input' folder.

>`tempo`: Tempo value represents beats per minute (bpm), eg: 100
 
 Encoding - sample usage
 ```
python3 main.py generate-dna -in sample.mid -tempo 100
```
>Running this command will generate a DNA sequence as a text file in 'Lamarck_DNA/output' folder.
### Decoding
> The DNA sequence is decoded to generate the audio output in MIDI, WAV and the musical score in a text file. The code maps the 4-letter codons back to corresponding musical notes with distinct pitch and lengths. The retrieved musical score is then converted to a MIDI file. The code uses -20 dBfs as the default value for volume (0.0 dBfs corresponds to the maximum value) and 100 as the default tempo. An audio file in WAVE format is generated from the MIDI file by computing the frequency (ƒ) of a note from the MIDI note number (d) as, F = 2<sup>(d-69)/12</sup> x 440Hz

 Command syntax to decode DNA into Midi/WAV/Music score
```
python3 main.py generate-music -in <input-dna-file> -out <mid,wav,txt> -tempo<beats per minute>
```
 Parameters

>`in`: The input DNA sequence ( a text file or *.fasta* file). "-in" parameter input file should be kept in the 'Lamarck_DNA/input' folder.
>`out`: Specify the output format/s () in the -out parameter. Output files will be generated in the 'LAMARCK_DNA/output' folder.
>`tempo`: Tempo value represents beats per minute (bpm), eg: 100
 
Decoding - sample usage
 ```
python3 main.py generate-music -in dna_seq.txt -out mid,wav,txt -tempo 100
```
>Running this command will generate the audio file in MIDI and WAVE formats and the music score (musical notes and durations) as a text file in 'Lamarck_DNA/output' folder.

## Testing Lamarckian-inheritance


To test the impact of Lamarckian inheritance, we have deployed different mutational regimes. The intention is to incorporate different noise patterns (mutations) in the actual audio, hence, the corresponding DNA sequences will be different from that of the original one, depending on the level of noise that is merged with. Different types of mutations are considered including synonymous, non-synonymous and single point mutations, at codon and musical element levels. A modified version of _Needleman_-_Wunsch_ algorithm is implemented to compare the distance between the derived audio files from different iterations. You can simulate the mutation-step as follows:

### Synonymous-mutation-workflow
> In this mutational scheme, the DNA sequences derived during successive iterations carry the same information, though it does not necessarily preserve the codon choice as codons are randomly selected by the code to encode, from 4 codon options. Hence, the information flow between DNA sequence and audio does not change any information at codon and musical score levels.

 Command syntax to generate synonymous mutation using a MIDI file
```
python3 main.py synonymous-wf -in <input-MIDI-file> -n <number-of-iterations> -tempo <beats per minute>
```
 Parameters

>`in`: The input MIDI file ( a single track, 4/4 time signature MIDI). "-in" parameter input file should be kept in the 'Lamarck_DNA/synonymous' folder.
>`n`: Number of iterations
>`tempo`: Tempo value represents beats per minute (bpm), eg: 100
 
 Synonymous mutation- sample usage
 ```
python3 main.py synonymous-wf -in sample.mid -n 5 -tempo 100
```
>Running this command will generate  'dna_*iteration-index*.txt' per iteration, in addition to the the un-mutated DNA sequence as 'dna_original.txt'  in the 'Lamarck_DNA/synonymous/output' folder. (Since we specified n=5 in the above example, 5 text files and the original-DNA file(un-mutated) will be generated after completing 5 iterations.)

### Random single point mutation-workflow
> In this scheme, a base at a random position in the DNA sequence is replaced with another base during consecutive iterations. This single point mutation may or may not result in a musical element transition, depending on how it alters the codon it belongs to. 

Command syntax to generate random single point mutation using a MIDI file
```
python3 main.py randomised-wf -in <input-MIDI-file> -n <number-of-iterations> -tempo <beats per minute>
```
 Parameters

>`in`: The input MIDI file ( a single track, 4/4 time signature MIDI). "-in" parameter input file should be kept in the 'Lamarck_DNA/randomised' folder.
>`n`: Number of iterations
>`tempo`: Tempo value represents beats per minute (bpm), eg: 100
 
Random single point mutation- sample usage
 ```
python3 main.py randomised-wf -in sample.mid -n 5 -tempo 100
```
>Running this command will generate  'dna_*iteration-index*.txt' per iteration, in addition to the the un-mutated DNA sequence as 'dna_original.txt'  in the 'Lamarck_DNA/randomised/output' folder. (Since we specified n=5 in the above example, 5 text files and the original-DNA file (un-mutated)  will be generated after completing 5 iterations.)

### Non-synonymous mutation-workflow
> This pattern of non-synonymous mutations at both codon and musical element levels in each iteration, continues in a feedback loop for *'n'* number of cycles, doubling the mutation rate at each round. At the initial round,  the encoder randomly selects a codon to code a musical element. In the second iteration, a musical element will be replaced with another and when re-coded to DNA which results in a mutation in the corresponding codon. Then, another mutation is introduced at the codon level by replacing a codon with a non-synonymous codon. When translated back to audio, this mutation results in a change in the corresponding musical element at that position. The process continues for *'n'* number of iterations. 

Command syntax to generate non-synonymous mutation using a MIDI file
```
python3 main.py mutation-wf -in <input-MIDI-file> -n <number-of-iterations> -tempo <beats per minute>
```
 Parameters

>`in`: The input MIDI file ( a single track, 4/4 time signature MIDI). "-in" parameter input file should be kept in the 'Lamarck_DNA/workflow' folder.
>`n`: Number of iterations
>`tempo`: Tempo value represents beats per minute (bpm), eg: 100
 
 Non-synonymous mutation- sample usage
 ```
python3 main.py mutation-wf -in sample.mid -n 5 -tempo 100
```
>After running the command the following actions take place:
( a )  *dna_mut_1.txt* will be created in the 'Lamarck_DNA/workflow/encoding' directory converting the *original music.mid* in the Lamarck_DNA/workflow' directory
( b ) *dna_mut_1.txt* is converted to *midi_1.mid*, *music_1.wav* and *music_note_1.txt* files and stored in the 'Lamarck_DNA/workflow/decoding/iter_1' directory
( c ) *midi_1.mid* file created in step (b) is converted back to *dna_mut_2.txt* and stored in the 'Lamarck_DNA/workflow/encoding' directory.
The above steps repeat for *n* number of times as mentioned in the command.

### Comparing-audio files 
> A modified version of *Needleman-Wunsch* algorithm is implemented to compare the distance between different audio files generated in different iterations. Two music-score text files are compared at a time. The scoring pattern implemented is as follows:
>- Exact match (If both the notes and durations at a given position are same) : 5
 >- Near match (If the notes are same but durations are different, at a given position) : 3
> - Mismatch (If both notes and durations are different at a given position) : 0
 >- Gap penalty (for insertions/deletions at a given position) : -2

Command syntax to compare music-score text files
```
python3 main.py compare-scores -in <input-music score-text files> 
```
 Parameters

>`in`: The input music-score text files to be compared . "-in" parameter input files should be kept in the 'Lamarck_DNA/input/scores' folder.

Compare music-score text files- sample usage
 ```
python3 main.py compare-scores -in original_score.txt,score1.txt,score2.txt,score3.txt
```
>After running the command the following actions take place:
>First file is considered as the original file. The rest of the files will be compared
against the first file.
In the above example, when running *'compare-scores -in original_score.txt, score1.txt, score2.txt, score3.txt',*  *score1.txt* will be compared against  *original_score.txt* first. Then *score2.txt* will be compared against  *original_score.txt* . Finally, *score3.txt* will be compared against  *original_score.txt*. 
Output log file '*comparisons.log`* is generated in 'Lamarck_DNA/output/scores' folder. the log file provides the alignment of each pair of music score-text files and corresponding score.

### Running the codebase
clone the 'Lamarck_DNA'  project to your local machine
```
git clone https://github.com/PooleLab/Lamarck_DNA.git
```
### Dependencies
Install all required python dependencies as per the table:

|Package|Version|Example|
|--|--|--|
|mido  | 1.2.10|conda install mido=1.2.10|
|numpy|latest|conda install numpy|
|pydub|0.25.1|conda install pydub=0.25.1|
|pip|latest|conda install pip|
|midiutil|1.2.1|pip install midiutil|
|wave|latest|pip install wave|

> Note: 
> * The system is based on an 88 key-keyboard and considers the Middle C (note number 60) as C4 (C in the 4th octave)
>  * The chosen 64 musical elements represent 16 notes (excluding the semitones) corresponding to the 4th, 5th and 6th octaves with four different lengths of 1 beat, ½ beat. ¼ beat and ⅛ of a beat
>  * Corresponding MIDI note-numbers range from 60 to 88 to make it a simple system
>  * As an experimental prototype, the musical score to be encoded is limited to a single track melody with 4/4 time signature.
### Helper-scripts
Following are the additional scripts that are used for certain edge-cases. 
#### Generating MIDI file from music-score
> If you need to generate a single track, 4/4 time signature MIDI file from a music-score text file, use the following command: 
```
Python3 main.py generate-midi -in <input-music score-text file> -tempo <beats per minute>
```
 Parameters

>`in`: The input music-score file ( a text file containing musical notes and durations). "-in" parameter input file should be kept in the 'Lamarck_DNA/input' folder.
>`tempo`: Tempo value represents beats per minute (bpm), eg: 100
 
 Generating MIDI file from music-score - sample usage
 ```
python3 main.py generate-midi -in music-score.txt -tempo 100
```
>Running this command will generate a MIDI file in 'Lamarck_DNA/output' folder.

#### Generating music-score from MIDI file
> If you need to generate the music-score as a text file from a single track, 4/4 time signature MIDI file use the following command: 
```
Python3 main.py generate-tabs -in <input-MIDI-file> -tempo <beats per minute>
```
 Parameters

>`in`: The input MIDI file ( ingle track, 4/4 time signature MIDI file). "-in" parameter input file should be kept in the 'Lamarck_DNA/input' folder.
>`tempo`: Tempo value represents beats per minute (bpm), eg: 100
 
 Generating music-score from MIDI file - sample usage
 ```
python3 main.py generate-tabs -in sample.mid -tempo 100
```
>Running this command will generate a music-score text file in 'Lamarck_DNA/output' folder.

#### MIDI-file-correction
> The MIDI-correction step is required to generate a MIDI file that contains the notes and durations that match our mapping scheme. The chosen 64 musical elements in our system represent 16 notes (excluding the semitones) corresponding to the 4th, 5th and 6th octaves with four different lengths of 1 beat, ½ beat. ¼ beat and ⅛ of a beat. If your MIDI file includes any full-notes or semitones from octaves below the 4<sup>th</sup> octave and above the 6<sup>th</sup> octave, those notes will be changed to corresponding notes in the 4<sup>th</sup>octave and 5<sup>th</sup> or 6<sup>th</sup> octaves respectively.  Similarly, any durations/note-lengths other than 1 beat, ½ beat. ¼ beat and ⅛ beat will be rounded to the nearest duration value. (Eg: If your MIDI file contains a note F9-0.628, it will be changed to F5-0.5). This supporting script is particularly useful when testing the Lamarckian inheritance where noise/mutations (corresponding to any random notes and durations) are added to an audio file.

 Command syntax to correct a MIDI file
```
python3 main.py correct-midi -in <input-MIDI-file> -tempo <beats per minute>
```
 Parameters

>`in`: The input MIDI file ( a single track, 4/4 time signature MIDI). "-in" parameter input file should be kept in the 'Lamarck_DNA/input' folder.
>`tempo`: Tempo value represents beats per minute (bpm), eg: 100
 
MIDI-correction - sample usage
 ```
python3 main.py correct-midi -in sample.mid -tempo 100
```
>Running this command will generate a corrected MIDI file in 'Lamarck_DNA/output' folder.

#### Splitting MIDI file with multiple-tracks
> As an experimental prototype, the musical score to be encoded is limited to a single track melody with 4/4 time signature. if your MIDI file include multiple tracks, it should be split to separate the tracks first, and then you can choose the melody track alone before testing with our system.

 Command syntax to split a multi-track MIDI file
```
python3 main.py split-midi -in <input-MIDI-file> -tempo <beats per minute>
```
 Parameters

>`in`: The input MIDI file ( a multi-track MIDI file). "-in" parameter input file should be kept in the 'Lamarck_DNA/input' folder.
>`tempo`: Tempo value represents beats per minute (bpm), eg: 100
 
Split a multi-track MIDI file - sample usage
 ```
python3 main.py split-midi -in sample.mid -tempo 100
```
>Running this command will generate separate MIDI files for each tracks and will be stored in 'Lamarck_DNA/output/midi-tracks' folder. 

---
