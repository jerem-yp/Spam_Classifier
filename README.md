# RealMail

## What is RealMail?
RealMail filters your emails, returning a sorted order of
by relevancy and urgency. It sorts through the clutter
of advertisements, promotional material, and bot-sent
mail to find the emails that you actually need to
see.

## Issue Introduction - My Take On Email Pollution
Personal email spaces are very polluted. This has largely
been controlled by mail apps such as Gmail, which
parse emails and remove spam as well as "labels" data.
However, I've noticed that some emails still tend to get
through these various labels, and show up in my main inbox.
This leads to lots of clutter.

As I've increased the usage of my email for use on
various sites, for various reward programs and whatnot,
I've noticed that I sometimes miss messages as they get
pushed farther underneath the stack of mail from 
non-urgent spam.


## Structure and General Notes
### Run Notes
* Requires Google Cloud access to Gmail API
    * Replace your files under INIT
* Languages
  * Python (3.11.3)
* Libraries
    * To Build Models
      * Numpy
      * Scikit-learn
    * NLP: NER entity-recognizer
      * SpaCy
      * NLTK
      * Flair

### File Structure
*/datasets*: Datasets spam classification model is trained on \
*/init*: Initialization files &rarr; Python INI and Google Client_Secret \
*/models*: Trained models. See setup for model versions \
*/user_data*: User data. Will be used in the future to improve NER
