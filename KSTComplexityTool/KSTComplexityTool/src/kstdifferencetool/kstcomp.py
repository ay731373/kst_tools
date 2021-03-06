#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is a tkinter tool for identifying differences between knowledge spaces.
"""
from tkinter import *
from tkinter.ttk import Frame, Label, Entry
import sys
import logging
import networkx as nx
import matplotlib.pyplot as pyplot

from kstdifferencetool import __version__

__author__ = "Milan Segedinac"
__copyright__ = "Milan Segedinac"
__license__ = "none"

_logger = logging.getLogger(__name__)


class GUI(Frame):
  
    def __init__(self):
        super().__init__()   
         
        self.initUI()

        
    def initUI(self):
      
        self.master.title("KST_comp")
        self.pack(fill=BOTH, expand=True)
        
        frame1 = Frame(self)
        frame1.pack(fill=X)
               
        btn_ks = Button(frame1, text="Knowledge space", command=self.browse_file_ks)
        btn_ks.pack(side=LEFT, padx=5, pady=5)

        self.e_ks = Entry(frame1)
        self.e_ks.pack(fill=X, padx=5, expand=True)
        
        frame3 = Frame(self,height=330)
        frame3.pack(fill=X)
        frame3.pack_propagate(False)
        
        lbl3 = Label(frame3, text="Complexity", width=10)
        lbl3.pack(side=LEFT, anchor=N, padx=5, pady=5)        

        self.txt_diff = Text(frame3)
        self.txt_diff.pack(fill=X, padx=5, expand=True)           

        frame4 = Frame(self)
        frame4.pack(fill=BOTH, expand=True)
        
        btn_construct = Button(frame4, text="Construct", command=self.construct_diff)
        btn_construct.pack(side=RIGHT)

    def browse_file_ks(self):
        from tkinter import filedialog

        Tk().withdraw() 
        self.e_ks.insert(0,filedialog.askopenfilename())

    def load_ks(self,path):
        data = []
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                data.append((int(line.split(',')[0].strip()),int(line.split(',')[1].strip())))
        return data

    def construct_diff(self):
        # real knowledge structure obtained by using IITA, without transitive closure
        real_knowledge_structure = nx.DiGraph(self.load_ks(self.e_ks.get()))

        # print(real_knowledge_structure.nodes())
        # transitive closure of the real knowledge structure
        tc_knowledge_structure = nx.DiGraph([(u,v,{'d':l}) for u,adj in nx.floyd_warshall(real_knowledge_structure).items() for v,l in adj.items() if l > 0 and l < float('inf')])

        # if there is any predecessor to the given node, than it is not in the fringe
        def in_fringe(node, graph):
            for edge in graph.edges():
                if edge[1] == node:
                    return False
            return True

        fringe = []
        complexity = []
        level = 1
        while tc_knowledge_structure.nodes():
            for node in tc_knowledge_structure.nodes():
                if in_fringe(node, tc_knowledge_structure):
                    fringe.append(node)
                    complexity.append((node,level))
            tc_knowledge_structure.remove_nodes_from(fringe)
            fringe = []
            level += 1

        self.txt_diff.delete(1.0,END)
        self.txt_diff.insert(END,""+str(complexity))
        # # ideal knowledge structure obtained by using Martin Schrepp's alogrithm, without transitive closure
        # ideal_knowledge_structure = nx.DiGraph(self.load_ks(self.e_expected_ks.get()))

        # # transitive closure of the ideal knowledge structure
        # tc_ideal_knowledge_structure = nx.DiGraph([(u,v,{'d':l}) for u,adj in nx.floyd_warshall(ideal_knowledge_structure).items() for v,l in adj.items() if l > 0 and l < float('inf')])

        # tc_ideal_minus_real = nx.difference(tc_ideal_knowledge_structure,tc_real_knowledge_structure)
        # # print("ideal minus real edges: ",tc_ideal_minus_real.edges())

        # tc_real_minus_ideal = nx.difference(tc_real_knowledge_structure,tc_ideal_knowledge_structure)
        # # print("real minus ideal edges: ",tc_real_minus_ideal.edges())
        # self.txt_diff.delete(1.0,END)
        # self.txt_diff.insert(END, ""+str(tc_real_minus_ideal.edges()))

def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(level=loglevel, stream=sys.stdout,
                        format=logformat, datefmt="%Y-%m-%d %H:%M:%S")


def main():
    """
    Main entry point allowing external calls
    """
    _logger.debug("Starting KSTDiff...")
    root = Tk()
    root.geometry("300x400+300+100")
    app = GUI()
    root.mainloop()  

def run():
    """Entry point for console_scripts
    """
    main()


if __name__ == "__main__":
    run()
