# -*- coding: utf-8 -*-
from itertools import izip, permutations, product, tee
import json

from django.test import TestCase

from openassessment.peer.models import Criterion, CriterionOption, Rubric
from openassessment.peer.serializers import RubricSerializer


#class TestHashing(TestCase):
#
#    def test_option_hashing_unicode_vs_bytes(self):
#        unicode_option = CriterionOption(
#            order_num=0, points=1, name="Bad", explanation=u"Can't understand it."
#        )
#        bytes_option = CriterionOption(
#            order_num=0, points=1, name=u"Bad", explanation=u"Can't understand it."
#        )
#        self.assertEqual(unicode_option.summary_hash(), bytes_option.summary_hash())
#
#    def test_non_latin_chars_hash(self):
#        # We're just making sure these don't throw exceptions
#        option = CriterionOption(
#            order_num=0, points=1, name=u"Áẃéśőḿé", explanation=u"ｷuﾚﾚ oｷ wﾉ刀"
#        )
#        option.summary_hash()
#
#        criterion = Criterion(
#            order_num=0, prompt=u"Ẅäṡ ïẗ äẅëṡöṁë?"
#        )
#        criterion.summary_hash()
#
#    def test_minor_option_differences(self):
#        combinations = {
#            'order_num': [0, 1],
#            'points': [0, 2],
#            'name': ["Sad", "sad", "Happy!"],
#            'explanation': ["Ewok death scene", "Ewoks dancing", "Ewoks Dancing"]
#        }
#        for a, b in model_combinations_by_pairs(CriterionOption, combinations):
#            self.assertNotEqual(
#                a.summary_hash(),
#                b.summary_hash(),
#                "{} and {} hash the same ({}), but shouldn't".format(
#                    a, b, a.summary_hash()
#                )
#            )
#
#    def test_child_objects_affect_hash(self):
#        pass


#class TestCriterion(TestCase):
#
#    @classmethod
#    def setUpClass(cls):
#        # This only runs once because Rubrics should never mutate. A great deal
#        # of our design depends on this assumption.
#        cls.project_rubric = cls._create_project_rubric()
#
#    @classmethod
#    def tearDownClass(cls):
#        cls.project_rubric.delete()
#
#    @classmethod
#    def _create_project_rubric(cls):
#        rubric = Rubric.objects.create(
#            prompt="Create a plan to deliver edx-tim!"
#        )
#
#        criteria = [
#            # Intentionally created out of order
#            Criterion(
#                rubric=rubric, order_num=1, prompt=u"Describe the architecture."
#            ),
#            Criterion(
#                rubric=rubric, order_num=0, prompt=u"Is the deadline realistic?"
#            ),
#        ]
#        rubric.criteria.add(*criteria)
#
#        arch_options = [
#            CriterionOption(
#                criterion=criteria[0], order_num=0, points=0, name="Crazy"
#            ),
#            CriterionOption(
#                criterion=criteria[0], order_num=1, points=1, name="Plausible"
#            ),
#            CriterionOption(
#                criterion=criteria[0], order_num=2, points=2, name="Solid"
#            ),
#        ]
#        deadline_options = [
#            CriterionOption(
#                criterion=criteria[1], order_num=0, points=0, name="No"
#            ),
#            CriterionOption(
#                criterion=criteria[1], order_num=1, points=2, name="Maybe"
#            ),
#            CriterionOption(
#                criterion=criteria[1], order_num=2, points=4, name="Yes"
#            ),
#        ]
#        # We're assigning it this way, but because of order_num, it should
#        # spit back out with the deadline criterion first.
#        criteria[0].options.add(*arch_options)
#        criteria[1].options.add(*deadline_options)
#
#        return rubric
#
#    def test_points_possible_calculation(self):
#        rubric = self.project_rubric
#        deadline_crit, arch_crit = rubric.criteria.all()
#
#        print json.dumps(RubricSerializer(rubric).data, indent=2)
#        1/0
#
#        self.assertEqual(deadline_crit.points_possible(), 4)
#        self.assertEqual(arch_crit.points_possible(), 2)
#        self.assertEqual(rubric.points_possible(), 5)
#
#    def test_hashing(self):
#        pass


def model_combinations_by_pairs(model_cls, template_dict):
    return (
        (model_cls(**a), model_cls(**b))
        for a, b in dict_product_by_pairs(template_dict)
    )

def dict_product_by_pairs(template_dict, all_permutations=False):
    """Returns iterable of (dict_a, dict_b) permutations based on template_dict.

    The idea of this method is that we often want to test things that are just a
    little different. For instance, if I want to test that a variation in any
    field will cause the hash to be generated differently, it's useful to return
    every possible combination of a set of field arguments. So it's basically
    what you would get if you were looking at every pair of entries that's
    generated by the innermost section of a giant nested for-loop.

    Args:
        template_dict (dict): Keys must be the keys you want in each generated
            dictionary. Values should be lists that will be cycled through when
            generating dicts in the output.
        all_permutations (bool): If True, will return every possible
            combination of produced pairs (n^2). False by default, so it will
            only return adjacent pairs.
    """
    def _pairwise(seq):
        """From s -> (s0,s1), (s1,s2), (s2, s3), ..."""
        a, b = tee(seq)
        next(b, None)
        return izip(a, b)

    all_dicts = dict_product(template_dict)

    if all_permutations:
        return permutations(all_dicts, 2)
    else:
        return _pairwise(all_dicts)

def dict_product(template_dict):
    """

    """
    all_value_combinations = product(*template_dict.values())
    keys = template_dict.keys()
    return (dict(zip(keys, values)) for values in all_value_combinations)

