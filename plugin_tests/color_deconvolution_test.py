#!/usr/bin/env python
# -*- coding: utf-8 -*-

###############################################################################
#  Copyright Kitware Inc.
#
#  Licensed under the Apache License, Version 2.0 ( the "License" );
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
###############################################################################

from tests import base

import numpy as np
import os
import skimage.io

from histomicstk.preprocessing import color_deconvolution as htk_dcv


TEST_DATA_DIR = os.path.join(os.environ['GIRDER_TEST_DATA_PREFIX'],
                             'plugins/HistomicsTK')


class MacenkoTest(base.TestCase):

    def test_macenko(self):
        im_path = os.path.join(TEST_DATA_DIR, 'Easy1.png')
        im = skimage.io.imread(im_path)[..., :3]

        w = htk_dcv.rgb_separate_stains_macenko_pca(im, 255)

        w_expected = [[0.089411,  0.558021, -0.130574],
                      [0.837138,  0.729935,  0.546981],
                      [0.539635,  0.394725, -0.826899]]

        np.testing.assert_allclose(w, w_expected, atol=1e-6)


class ColorDeconvolutionTest(base.TestCase):

    def test_roundtrip(self):
        im_path = os.path.join(TEST_DATA_DIR, 'Easy1.png')
        im = skimage.io.imread(im_path)[..., :3]

        w = np.array([[0.650, 0.072, 0],
                      [0.704, 0.990, 0],
                      [0.286, 0.105, 0]])

        conv_result = htk_dcv.color_deconvolution(im, w, 255)

        im_reconv = htk_dcv.color_convolution(conv_result.StainsFloat,
                                              conv_result.Wc, 255)

        np.testing.assert_allclose(im, im_reconv, atol=1)
