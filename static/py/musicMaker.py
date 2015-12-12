from bs4 import BeautifulSoup as bs
from chording.chord_main import *
from percussion.extract_percussion import return_pattern as rp
from algo.N_gram import N_gram_main_function_multiple as ngram
from algo.Association import asso_main as am
import re

class Music:
	def __init__(self,addr,main_melody=None):
		with open(addr,'r') as f:
			mscx = bs(f.read(),'xml')
		self.music = mscx
		self.main_melody = main_melody

	def getChords(self):
		return findChords(self.music,self.main_melody)
		
	def getPichedStaffs(self):
		l = []
		fst = findStaffInfo(self.music)
		for staff in fst:
			l.append(PitchedStaff(staff,fst[staff]['content'],fst[staff]['instrument']))
		return l
		
	def getPercussions(self):
		pers = rp(self.music)
		l = []
		for staff in pers:
			l.append(PercussionStaff(staff,pers[staff]))
		return l
	
	def getGram(self,pattern,num,com):
		return ngram(pattern,num,com)

class Staff:
	def __init__(self,stid,content):
		self.id = re.match('.*?(\d+)',stid).group(1)
		self.content = content
	
	def joinByMeasure(self):
		m_dic = {}
		for measure in self.content:
			m_num = int(re.match('.*?(\d+)',measure).group(1))
			m_dic.update({m_num:self.content[measure]})
		returned_dic = {}
		for num in sorted(m_dic):
			for track in m_dic[num]:
				if returned_dic.get(track) is None:
					returned_dic.update({track:m_dic[num][track]})
				else:
					returned_dic[track] += m_dic[num][track]
		return returned_dic

		
class PercussionStaff(Staff):
	def __init__(self,stid,content,sep_1=0.2,sep_2=0.07):
		Staff.__init__(self,stid,content)
		self.pattern,self.patternDetail = am(self.content,sep_1,sep_2)
		self.instrument = 'percussionType'
	
	def pattern(self):
		return self.pattern
	def patternDetail(self):
		return self.patternDetail
		
	def resetSep(self,sep_1,sep_2):
		self.pattern,self.patternDetail = am(self.content,sep_1,sep_2)
		
class PitchedStaff(Staff):
	def __init__(self,stid,content,instrument):
		Staff.__init__(self,stid,content)
		self.instrument = instrument