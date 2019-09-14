# -*- coding: utf-8 -*-
""" Spellchecker class

This module creates the base ldt spellchecker class, based on
`cyhunspell <https://github.com/rfk/pyenchant>`_ . It makes use of hunspell
dictionaries found on the user system. If more dictionaries are needed,
they need to be added by the user.

Basic functionality:

    * target language spellchecking
    * checking if a word as "foreign", i.e. if the queried word has an entry
      in a number of spellchecker dictionaries for a set of other
      pre-defined languages;

Todo:

    * add names from wiki namespaces
    * not to check words with _

"""

import functools
import unicodedata

from difflib import SequenceMatcher

from hunspell import Hunspell
from hunspell import HunspellFilePathError

from ldt.dicts.dictionary import Dictionary
from ldt.load_config import config
from ldt.helpers.resources import lookup_language_by_code
from ldt.helpers.exceptions import LanguageError

class Spellchecker(Dictionary):
    """The base spellchecker class (CyHunspell-based)."""

    def __init__(self, language=config["default_language"],
                 foreign_languages=config["foreign_languages"],
                 hunspell_path = config["language_resources"]["hunspell_path"]):
        """Initializaing a spellchecker for the target and a number of
        frequent "foreign" languages.

        Attempting to establish relations between word pairs would make
        little sense if one word was foreign - but e.g. Spanish words are
        fairly frequent in American English corpora. LDT provides an option to
        define what foreign languages could be expected to be frequent in
        the input. They would then be disregarded in subsequent analysis.

        Args:
            language (str): the target language, either a full name
                ("english"), 2-letter code ("en"), or a spellchecker
                resource code for a specific sublanguage ("en_US").
            foreign_languages (tuple): other languages that could be expected
                to be relatively frequent in the input. Ditto for the format.

        """

        super(Spellchecker, self).__init__(language=language)

        #: (str): The main language of the spellchecker.
        self.language = check_language(language)
        self.hunspell_path = hunspell_path
        #: (Hunspell spellchecker object): The spellchecker for the main
        # language.
        self.target = Hunspell(self.language,
                               hunspell_data_dir=self.hunspell_path)

        def _set_language(self, language):
            """Setter for the language attribute."""
            self.language = check_language(language)
            self.target = self._hunspell_dict(self.language)

        #: list(str): the language(s) to be considered "foreign".
        self.foreign_languages = [check_language(lang) for
                                  lang in foreign_languages]

        #: list(spellechecker objects): the checkers for the foreign language(s).
        self.foreign = []
        for lang in self.foreign_languages:
            self.foreign.append(self._hunspell_dict(lang))

    def _hunspell_dict(self, language):
        """ Helper for CyHunspell dictionary initialization.

        Args:
            language (str): the language of the dictionary.

        Returns:
                CyHunspell spellchecker object for a given language

        Raises:
            LanguageError: the language is unavailable or improperly formatted
        """

        error = "No spellchecking dictionary for language " + language + \
                ". Either the dictionary is unavailable in Hunspell resources " \
                "on your system, or the language argument is not formatted as " \
                "required by Hunspell (e.g. 'en', 'en_US')."
        try:
            return Hunspell(language, hunspell_data_dir=self.hunspell_path)
        except HunspellFilePathError:
            raise LanguageError(error)

    def is_a_word(self, word):
        """Returns *True* is the word is in the dictionary.

        Example:
            >>> test_dict = ldt.dicts.spellcheck.Spellchecker()
            >>> test_dict.is_a_word("cat")
            True

        Args:
            word (str): the word to check.

        Returns:
            (bool): *True* if the word is in the spellchecker dictionary for
            the target language.
        """
        return self.target.spell(word)


    @functools.lru_cache(maxsize=config["cache_size"])
    def in_foreign_dicts(self, word):
        """Returns True if the word is found in the spellchecker resources
        for the specified foreign languages.

        Example:
            >>> test_dict = ldt.dicts.spellcheck.Spellchecker()
            >>> test_dict.in_foreign_dicts("chocolat")
            False

        Args:
            word (str): the word to check

        Returns:
            (bool): True if the word is found in the "foreign" dictionaries.
        """

        for spelldict in self.foreign:
            if spelldict.spell(word):
                return True
        return False

    # pylint: disable=no-self-use
    def filter_by_charset(self, word, include=["latin", "digit"],
                          exclude=["with"]):
        """Simple filter by character type: returns False for words with
        letters from any Unicode charset other than the the listed.

        Example:
            >>> test_dict = ldt.dicts.spellcheck.Spellchecker()
            >>> test_dict.filter_by_charset("猫", "LATIN")
            False

        Args:
            word (str): the word to check;
            charsets (list): the character categories as returned by python
            unicodedata (`full list of codes
            <http://unicode.org/charts/charindex.html>`)).  Useful values include:

                * [latin] for all Latin characters
                * [latin, with] to exclude diacritics
                * [cyrillic]
                * [arabic]
                * [korean]
                * [cjk] (unified ideograms)
                * [hyphen-minus, apostrophe, digit]
                * etc.

        Returns:
            (bool): True if the word's characters are entirely within the
                specified charsets
        """
        include = [x.lower() for x in include]
        exclude = [x.lower() for x in exclude]
        for character in word:

            name = unicodedata.name(character).lower()
            if " " in name:
                name = set(name.split())
            else:
                name = set([name])

            if not name.intersection(set(include)):
                return False
            elif name.intersection(set(exclude)):
                return False
        return True

    def suggest(self, word):
        """Suggesting alternative spellings for the word.

        Example:
            >>> test_dict = ldt.dicts.spellcheck.Spellchecker()
            >>> test_dict.suggest("iwth")
            ['with']

        Args:
            word (str): the word to check

        Returns:
            (list): a list of alternative spellings
        """

        return self.target.suggest(word)

    # pylint: disable=no-self-use
    def get_opcode_alignment(self, misspelling, word):
        """Helper for aligning a word with its potential misspelling

        Example:
            >>> ldt.dicts.spellcheck.get_opcode_alignment("grammer", "grammar")
            {'deletes': [],
             'inserts': [],
             'misspelling': 'grammE_r',
             'replaces': [('e', 'a')],
             'word': 'gramm_Ar'}
            >>> ldt.dicts.spellcheck.get_opcode_alignment("generaly",
            "generally")
            {'deletes': [],
             'inserts': ['l'],
             'misspelling': 'general_y',
             'replaces': [],
             'word': 'generalLy'}

        Args:
            misspelling (str): a potentially misspelled word
            word (str): the word to check

        Returns:
            (dict): a dictionary with "word" and "misspelling" keys for the
            aligned strings, brought to equal length, with mismatching
            characters signaled by underscores and capital letters. Insertions,
            deletions and replacements are also listed under separate keys.
        """

        res = {"misspelling": [], "word": [], "deletes": [], "inserts": [],
               "replaces": []}

        sequence = SequenceMatcher(None, misspelling, word)
        # pylint: disable=invalid-name
        for tag, i1, i2, j1, j2 in sequence.get_opcodes():

            if tag == "equal":
                res["misspelling"].append(misspelling[i1:i2])
                res["word"].append(word[j1:j2])
            if tag == "delete":
                if misspelling[i1:i2]:
                    res["misspelling"].append(misspelling[i1:i2].upper())
                    res["word"].append("_" * len(misspelling[i1:i2]))
                    res["deletes"].append(
                        max([misspelling[i1:i2], word[j1:j2]],
                            key=len))
            if tag == "insert":
                if word[j1:j2]:
                    res["misspelling"].append("_" * len(word[j1:j2]))
                    res["word"].append(word[j1:j2].upper())
                    res["inserts"].append(
                        max([misspelling[i1:i2], word[j1:j2]],
                            key=len))
            if tag == "replace":
                if misspelling[i1:i2]:
                    res["misspelling"].append(misspelling[i1:i2].upper())
                    res["word"].append("_" * len(misspelling[i1:i2]))
                if word[j1:j2]:
                    res["word"].append(word[j1:j2].upper())
                    res["misspelling"].append("_" * len(word[j1:j2]))
                res["replaces"].append((misspelling[i1:i2], word[j1:j2]))
        res["misspelling"] = "".join(res["misspelling"])
        res["word"] = "".join(res["word"])
        return res


def check_language(language):
    """CyHunspell accepts languages as 2-letter codes (e.g. "en"),
    or in fr_FR format of Hunspell dictionaries. This helper either formats
    the language to 2-letter code, or raises an error if it does not look
    like a Hunspell dictionary.

    Args:
        language (str): the language to look up

    Returns:
        (str): language formatted as 2-letter code

    """

    if len(language) > 2 and language[2] != "_":
        language = lookup_language_by_code(language, reverse=True)
    return language
