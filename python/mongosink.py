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
    def __init__(self, host, database, collection, nfloatsinks, nsamp_before, nsamp_after):
        gr.sync_block.__init__(self,
            name="mongosink",
            in_sig=[np.int8, np.float32, np.float32, np.int8],
            out_sig=None)

        self.hist_samp = nsamp_before + nsamp_after
        self.set_history(self.hist_samp)
        self.nsamp_before = nsamp_before
        self.nsamp_after = nsamp_after

        self.host = host
        self.database = database
        self.collection = collection

        self.packets = pymongo.MongoClient(self.host)[self.database][self.collection]

    def work(self, input_items, output_items):
        in0 = input_items[0]
        in1 = input_items[1]
        in2 = input_items[2]
        in3 = input_items[3]
        
        # All ones in in0 are triggers. TODO expand logic to also support a holdoff
        for i in np.nonzero(in0[self.nsamp_before: -self.nsamp_after])[0]:
            if self.nitems_read(0) + i > 600:
                i += self.nsamp_before
                self.packets.save({'time': time.time(), 'sample_nr': self.nitems_read(0) + i - self.hist_samp + 1, 'samples1': in1[i - self.nsamp_before:i + self.nsamp_after].tolist(), 'samples2': in2[i - self.nsamp_before:i + self.nsamp_after].tolist(), 'msg': in3[i - self.nsamp_before:i + self.nsamp_after].tolist()})

        return len(in0[self.hist_samp:])
