#!/usr/bin/env python

import yaml
import re
import copy

class vdy:
    REG_VARIABLE = r'\$[a-zA-Z0-9_]+'
    REG_VARIABLE_ONLY = r'^\$([a-zA-Z0-9_]+)$'

    SYMBOL_SLASH = '/'

    TYPE_DICT = 'DICT'
    TYPE_LIST = 'LIST'
    TYPE_VALUE = 'VALUE'
    TYPE_NONE = 'NONE'

    KEYWORD_IMPORT = 'IMPORT'

    def __init__(self, vdyFileName=None):
        self.vdyFileName = vdyFileName
        self.yamlDoc = dict()
        self.variDoc = dict()
        if vdyFileName != None:
            if type(vdyFileName) is str: self.yamlDoc.update(self.handleDoc(vdyFileName))
            elif type(vdyFileName) is list:
                for f in vdyFileName:
                    self.yamlDoc.update(self.handleDoc(f))
            else: pass
            #self.handleValue(None, self.TYPE_NONE, None, self.yamlDoc, self.referVariDoc, self.dummy)

    def handleDoc(self, fileName):
        origDoc = self.importYaml(fileName)
        origPath = self.getPath(fileName)
        for f in origDoc.get(self.KEYWORD_IMPORT, []): origDoc.update(self.handleDoc(origPath+f))
        self.handleValue(None, self.TYPE_NONE, None, origDoc, self.generateVariDoc, self.dummy)
        #self.handleValue(None, self.TYPE_NONE, None, origDoc, self.referVariDoc, self.dummy)
        return origDoc

    def getPath(self, fileName):
        return  self.SYMBOL_SLASH.join(fileName.split(self.SYMBOL_SLASH)[0:-1]) + self.SYMBOL_SLASH

    def importYaml(self, yamlName):
        with open(yamlName, 'r') as f: doc = yaml.safe_load(f.read())
        return doc

    def handleValue(self, p, t, k, v, b, a):
        if type(v) is dict: self.walkDict(p, t, k, v, b, a)
        elif type(v) is list: self.walkList(p, t, k, v, b, a)
        else: self.walkValue(p, t, k, v, b, a)

    def walkDict(self, point, ptype, key, value, prefunc, postfunc):
        for k, v in value.iteritems():
            prefunc(point, ptype, key, value)
            self.handleValue(value, self.TYPE_DICT, k, v, prefunc, postfunc)
            postfunc(point, ptype, key, value)

    def walkList(self, point, ptype, key, value, prefunc, postfunc):
        for k in range(len(value)):
            prefunc(point, ptype, key, value)
            self.handleValue(value, self.TYPE_LIST, k, value[k], prefunc, postfunc)
            postfunc(point, ptype, key, value)

    def walkValue(self, point, ptype, key, value, prefunc, postfunc):
        prefunc(point, ptype, key, value)
        postfunc(point, ptype, key, value)

    def generateVariDoc(self, point, ptype, key, value):
        if ptype == self.TYPE_DICT: self.variDoc[key] = value

    def referVariDoc(self, point, ptype, key, value):
        if type(value) is dict: pass
        elif type(value) is list: pass
        elif type(value) is str:
            newValue = self.referVari(value)
            if type(key) is str:
                newKey = self.referVari(key)
                if newKey != key:
                    del point[key]
                    point[newKey] = newValue
                else: point[key] = newValue
            else: point[key] = newValue
        else: pass

    def referVari(self, value):
        value = self.referVariOnly(value)
        if type(value) is str: return self.referVariStr(value)
        else: return value

    def referVariOnly(self, value):
        m = re.search(self.REG_VARIABLE_ONLY, value.strip())
        while m:
            if m.group(1) in self.variDoc.keys():
                value = self.variDoc[m.group(1)]
                if type(value) is str:
                    m = re.search(self.REG_VARIABLE_ONLY, value.strip())
                else:
                    #self.handleValue(None, self.TYPE_NONE, None, value, self.referVariDoc, self.dummy)
                    m = False
            else: m = False
        return value

    def referVariStr(self, value):
        newValue = value
        while re.search(self.REG_VARIABLE, newValue):
            s, e = [(m.start(), m.end()) for m in re.finditer(self.REG_VARIABLE, newValue)][0]
            newValue = newValue[:s] + str(self.variDoc.get(newValue[s+1:e], newValue[s+1:e])) + newValue[e:]
        return newValue

    def dummy(self, point, ptype, key, value): pass

    def assign(self, variable=None):
        if variable != None:
            self.handleValue(None, self.TYPE_NONE, None, variable, self.referVariDoc, self.dummy)
            return variable
        else:
            self.handleValue(None, self.TYPE_NONE, None, self.yamlDoc, self.referVariDoc, self.dummy)
            return self.yamlDoc

    def clone(self, other):
        self.vdyFileName = str(other.vdyFileName)
        self.yamlDoc = copy.deepcopy(other.yamlDoc)
        self.variDoc = copy.deepcopy(other.variDoc)
        return self

    def join(self, variable):
        if type(variable) is dict:
            self.yamlDoc.update(variable)
            self.handleValue(None, self.TYPE_NONE, None, self.yamlDoc, self.generateVariDoc, self.dummy)
            #self.handleValue(None, self.TYPE_NONE, None, self.yamlDoc, self.referVariDoc, self.dummy)
        return self

    def clearVariDoc(self):
        self.variDoc.clear()
        return self

    def __str__(self):
        return str(self.yamlDoc)