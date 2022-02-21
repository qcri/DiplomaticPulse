## How to contribute to Diplomatic Pulse code

There are 4 ways you can contribute to Diplomatic Pulse project:
- Implementing new spiders to scrape  ".doc", ".img", ".jpg" contents.
- Improving string dates parsing to handle possible unhandled string dates;
- Improving formating html text ;  
- Contributing to the documentation;

Follow these steps to submit your code contribution.

### Step 1. Open an issue

If the changes are minor (simple bug fix or documentation fix), then feel free
to open a PR without discussion. Otherwise, we recommend opening an issue (if one doesn't already
exist) and discuss your proposed changes. This way, we can give you feedback
and validate the proposed changes. Here is a template


Write a full paragraph describing the feature;
Provide a code snippet that demonstrates its future use;
In case this is related to a paper, please attach a link;
Attach any additional information (drawings, screenshots, etc.) you think may help.


Fork the repository by clicking on the 'Fork' button on the repository's page. This creates a copy of the code under your GitHub user account.

Clone your fork to your local disk, and add the base repository as a remote:

```python
git clone git@github.com:qcri/DiplomaticPulse.git
cd Diplomaticpulse
git remote add upstream  https://github.com/<your-github-username>/qcri/DiplomaticPulse.git
```

Create a new branch to hold your development changes:

```python
git checkout -b branch-name
```

Do not work on the master branch.

Set up a development environment by running the following command in a virtual environment:

```python
python3 -m venv diplomaticpulse-env
source diplomaticpulse-env/bin/activate
(diplomaticpulse-env) pip install --upgrade pip
(diplomaticpulse-env) cd diplomaticpulse
(diplomaticpulse-env) pip install -e .
```

Make sure you have `requirements.txt` installed, so you can use `pylint`.

```python
(diplomaticpulse-env) pip install -r requirements.txt

```

### Step 2. Make code changes

```python
(diplomaticpulse-env) pylint --rcfile=.pylintrc path/to/changed/file
```

And darglint by

```python
(diplomaticpulse-env) darglint -s google path/to/changed/file
```


### Step 3. Create a pull request

Once the change is ready, open a pull request from your branch in your fork to
the master branch in [diplomaticpulse](https://github.com/qcri/diplomaticpulse).

### Step 4. Code review

Before waiting for a reviewer to see the pull request, please look into the [CI pipeline](https://github.com/qcrisw/diplomaticpulse/actions) ran on your branch to see if there are any errors.

### Step 5. Merging

Once the pull request is approved, a `ready to pull` tag will be added to the
pull request. A team member will take care of the merging.

