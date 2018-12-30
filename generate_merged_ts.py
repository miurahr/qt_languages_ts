#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET
import sys

def main():
    lang = sys.argv[1]
    if lang == "zh_CN":
        targets = ["assistant" "designer" "linguist" "qt_help" "qt"]
    else:
        targets = ["assistant" "designer" "linguist" "qmlviewer"  "qt_help" "qt" "qtbase" "qtdeclarative" "qtmultimedia" "qtquick1" "qtquickcontrols" "qtscript" "qtserialport" "qtwebsockets" "qtxmlpatterns"]

    destTree = ET.parse('qtall_'+lang+'.ts')
    destRoot = destTree.getroot()
    for target in targets:
        srcTree = ET.parse(target+'_'+lang+'.ts')
        srcRoot = srcTree.getroot()
        for srcContext in srcRoot.findall('context'):
            hasThisContext = False
            srcName = srcContext.find('name').text
            for destContext in destRoot.findall('context'):
                destName = destContext.find('name').text
                if srcName == destName:
                    hasThisContext = True
                    for srcMessage in srcContext.findall('message'):
                        hasThisMessage = False
                        srcSource = srcMessage.find('source').text
                        for destMessage in destContext.findall('message'):
                            destSource = destMessage.find('source').text
                            if srcSource == destSource:
                                hasThisMessage = True
                                pass
                        if not hasThisMessage:
                            if not srcRoot.attrib['language'].startswith(lang):
                                srcTranslation = srcMessage.find('translation')
                                srcTranslation.text = ''
                                srcTranslation.set('type', 'unfinished')
                            destContext.append(srcMessage)
            if not hasThisContext:
                if not srcRoot.attrib['language'].startswith(lang):
                    for srcTranslation in srcContext.iter('translation'):
                        srcTranslation.text = ''
                        srcTranslation.set('type', 'unfinished')
                destRoot.append(srcContext)

        for destMessage in destRoot.iter('message'):
            for destLocation in destMessage.findall('location'):
                destMessage.remove(destLocation)

    destTree.write('qt_'+lang+'.ts', encoding='utf-8')

if __name__ == "__main__":
    main()

