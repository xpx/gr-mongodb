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

class streamsink(gr.sync_block):
    """
    docstring for block streamsink
    """
    def __init__(self, host, database, collection, nfloatsinks, nsamp_before, nsamp_after):
        in_vec = [np.float32]
        for i in range(nfloatsinks):
            in_vec.append(np.float32)
        gr.sync_block.__init__(self,
            name="streamsink",
            in_sig=in_vec,
            out_sig=None)

        self.hist = nsamp_before + nsamp_after
        self.set_history(self.hist)
        self.nsamp_before = nsamp_before
        self.nsamp_after = nsamp_after

        self.host = host
        self.database = database
        self.collection = collection

        self.mongo_sink = pymongo.MongoClient(self.host)[self.database][self.collection]


    def work(self, input_items, output_items):
        in0 = input_items[0]

        tags = self.get_tags_in_window(0, self.nsamp_before, len(in0) - self.nsamp_after)
    
        for tag in tags:
            # calculate relative offset for tag in input items
            relative_offset = tag.offset - self.nitems_read(0) 
            print tag.key, tag.value, tag.offset, relative_offset
            self.mongo_sink.save({'time': time.time(), 'nitems_read': self.nitems_read(0), 'relative_offset': relative_offset, 'tag_key': str(tag.key), 'tag_value': str(tag.value), 'tag_offset': tag.offset, 'data1': in0[relative_offset - self.nsamp_before:relative_offset + self.nsamp_after].tolist()})

        return len(input_items[0])

