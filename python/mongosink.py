#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2014 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

import time
import numpy as np
from gnuradio import gr
import pymongo

class mongosink(gr.sync_block):
    """
    docstring for block mongosink
    """
    def __init__(self, delay, hist_samp):
        gr.sync_block.__init__(self,
            name="mongosink",
            in_sig=[np.int8, np.float32, np.float32, np.int8],
            out_sig=None)

        self.set_history(hist_samp)
        self.delay = delay
        self.hist_samp = hist_samp

        self.tot_samples = 0

        self.packets = pymongo.MongoClient('localhost')['gnu_adsb']['packets']


    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        in2 = input_items[2]
        in3 = input_items[3]
        
        for i in np.nonzero(in0[self.hist_samp:])[0]:
            if self.tot_samples + i > 600:
                self.packets.save({'time': time.time(), 'sample_nr': self.tot_samples + i, 'samples1': in1[i:i + self.hist_samp].tolist(), 'samples2': in2[i:i + self.hist_samp].tolist(), 'msg': in3[i - 112 * 4:i:4].tolist()})

        self.tot_samples += len(in1[:-self.hist_samp])
        return len(in1[:-self.hist_samp])
