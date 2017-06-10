# -*- coding: utf-8 -*-
import click
import time
from random import choice, shuffle


'''
Creates a mashup from a list of headlines (or plain sentences), based on a set of separators.

The idea is to provide separators like "and", "with", "the", and break two headlines to re-join them into a new sentence. E.g.:

    Theresa May throws Tories into disarray
    UN Inspectors move into Kinshasa

If the word "into" is in the separators file, we'd obtain "Theresa May throws Tories into Kinshasa" or "UN Inspectors move into disarray". It selects lines randomly.

The point is to have a decent set of headlines and a number of separators so that unpredictable combinations can come up.

TODO:
    - split sentences via regexes with \b and lowercase

'''


def get_word_matches(word, lines):
    '''Gathers the lines that contain a certain word.'''
    matches = []
    for headline in lines:
        words = headline.split(" ")
        if word in words:
            matches.append(headline)
    return matches


def test_common_word(word, lines):
    '''Ensures that the separator matches two of the input lines.'''
    matches = get_word_matches(word, lines)
    if not len(matches) > 1:
        return False
    return True


def get_dada_headline(lines, separators, min_words=3):
    '''Main function that takes a list of strings with headlines and another with separators.
    The minimum amount of words for an acceptable outcome can also be set.'''
    # pick a separator
    common_word = choice(separators).strip()
    # ensure there is at least two lines with this separator word
    while not test_common_word(common_word, lines):
        common_word = choice(separators).strip()
    # get two lines
    matches = get_word_matches(common_word, lines)
    shuffle(matches)
    line1 = matches.pop().strip()
    line2 = matches.pop().strip()
    # ensure they're not equal
    while not line1 != line2:
        try:
            line2 = matches.pop().strip()
        except IndexError:
            # no more lines, try again
            return get_dada_headline(lines, separators)

    # break the lines at the separator
    part1 = line1.split(" %s " % common_word)[0].strip()
    part2 = line2.split(" %s " % common_word)[-1].strip()
    # join them into a new combination
    output = "%s %s %s" % (part1, common_word, part2)
    # ensure we don't get a result that is the same as one of the lines
    if output == line1 or output == line2:
        return get_dada_headline(lines, separators, min_words)
    # ensure it has enough words
    if len(output.split(" ")) < min_words:
        return get_dada_headline(lines, separators, min_words)
    return output


@click.command()
@click.argument('lines_file', type=click.File('rb'), required=True)
@click.argument('separators_file', type=click.File('rb'), required=True)
@click.option('-m', '--at-least', help="Minimum number of words", default=3)
def run(lines_file, separators_file, at_least):
    """This script takes a file with source lines and another with separator words."""
    lines = [l.strip() for l in lines_file.readlines()]
    separators = separators_file.readlines()
    outcome = get_dada_headline(lines, separators, min_words=at_least)
    print
    print('   ' + outcome)
    print


if __name__ == "__main__":
    run()
