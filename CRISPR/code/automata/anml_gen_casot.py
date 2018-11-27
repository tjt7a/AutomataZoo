#!/usr/bin/python
import sys

if len(sys.argv) != 4 :
    print "USAGE: python anml_gen_casot.py <infile> <dist1> <dist2>"
    sys.exit(1)

filename = sys.argv[1]
dist1 = int(sys.argv[2])
dist2 = int(sys.argv[3])

def start(start_id,length, length2, dist, dist2, character_upper, character_lower):
    if dist>=2 and dist <= length/2:
        for i in range(1,length+1):
            if i%length == 1:
                print '        <state-transition-element id="%d" symbol-set="[%s%s]" start="all-input">' %(start_id+i,character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                print "        </state-transition-element> "

                print '        <state-transition-element id="%d" symbol-set="[^%s%s]" start="all-input">' %(start_id+i+length-dist,character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1+length-dist)
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1+length-dist+length-dist)
                print "        </state-transition-element> "
                i=i+1

            elif i%length==0:
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[length-1], character_lower[length-1])
                #print '                	<report-on-match/>'
                print '                <activate-on-match element="%d"/>' %(start_id+101)
                print '                <activate-on-match element="%d"/>' %(start_id+101+length2-dist2)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*dist*(length-dist)),character_upper[length-1], character_lower[length-1])
                #print '                	<report-on-match/>'
                print '                <activate-on-match element="%d"/>' %(start_id+101)
                print '                <activate-on-match element="%d"/>' %(start_id+101+length2-dist2)
                print "        </state-transition-element> "

            elif i%length > dist and i%length < (length-dist):
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                print "        </state-transition-element> "
                for j in range(1,dist):
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+(2*j)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                j = j+1
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+(2*dist)*(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+(2*dist)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+(2*dist)*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1

            elif i%length>1 and i%length<=dist:

                if i%length==dist:
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                    print "        </state-transition-element> "
                    for j in range(1,dist):
                        print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                        print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+(2*j)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                    j=j+1
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*dist)*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1

                else:
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                    print "        </state-transition-element> "
                    for j in range(1,i):
                        print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                        print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*j*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                    j=j+1
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1

            else:
                #last rows with empty elements
                if i%length > length-dist:
                    ####should I +1 or not?
                    for j in range(1, length-i%length+1):
                        #others
                        if j < (length-i%length):
                            print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*(dist-j)-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j))*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)+1)*(length-dist)+1)
                            print "        </state-transition-element> "
                            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+(2*(dist-j))*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j))*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)+1)*(length-dist)+1)
                            print "        </state-transition-element> "
                        #first two
                        else:
                            print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*(dist-j)-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+2)*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+3)*(length-dist)+1)
                            print "        </state-transition-element> "
                            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(dist-j)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+2)*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+3)*(length-dist)+1)
                            print "        </state-transition-element> "

                    #last two STE in the column
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*dist-1+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*dist*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+2*dist*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1

                #last colum with full elements
                else:
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(length-dist)*2+1)
                    print "        </state-transition-element> "
                    for j in range(1,dist):
                        print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+2*j*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                        print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+ 2*j*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+ 2*j*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+ (2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "

                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+2*dist*(length-dist)+1)
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*dist*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+2*dist*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1

    if dist==1:
        for i in range(1,length+1):
            if i % length == 0:
                #print length-1
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+length-dist),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+101)
                print '                <activate-on-match element="%d"/>' %(start_id+101+length2-dist2)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(length-dist)),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+101)
                print '                <activate-on-match element="%d"/>' %(start_id+101+length2-dist2)
                print "        </state-transition-element> "

            elif i % length == (length-1):
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1

            elif i%length==1:
                #not always all-input
                print '        <state-transition-element id="%d" symbol-set="[%s%s]" start="all-input">' %(start_id+i,character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]" start="all-input">' %((start_id+i+length-dist),character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1


            else:
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1



    if dist==0:
        if i % length == 0:
            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[length-1], character_lower[length-1])
            print '                <activate-on-match element="%d"/>' %(start_id+101)
            print '                <activate-on-match element="%d"/>' %(start_id+101+length2-dist2)
            print "        </state-transition-element> "
        if i%length==1:
            print '        <state-transition-element id="%d" symbol-set="[%s%s]" start="all-input">' %(start_id+i,character_upper[0], character_lower[0])
            print '                <activate-on-match element="%d"/>' %(start_id+i+1)
            print "        </state-transition-element> "

        else:
            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
            print '                <activate-on-match element="%d"/>' %(start_id+i+1)
            print "        </state-transition-element> "
            i=i+1
    if dist > length/2 and dist < length-1:
        for i in range(1,length+1):
            if i%length == 1:
                print '        <state-transition-element id="%d" symbol-set="[%s%s]" start="all-input">' %(start_id+i,character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                print "        </state-transition-element> "

                print '        <state-transition-element id="%d" symbol-set="[^%s%s]" start="all-input">' %(start_id+i+length-dist,character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1+length-dist)
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1+length-dist+length-dist)
                print "        </state-transition-element> "
                i=i+1

            elif i%length==0:
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+101)
                print '                <activate-on-match element="%d"/>' %(start_id+101+length2-dist2)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*dist*(length-dist)),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+101)
                print '                <activate-on-match element="%d"/>' %(start_id+101+length2-dist2)
                print "        </state-transition-element> "

            elif i%length > (length-dist) and i%length < dist:
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+((i%length-(length-dist))*2-1)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+1)*(length-dist)+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+2)*(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i+((i%length-(length-dist))*2)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+1)*(length-dist)+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+2)*(length-dist)+1)
                print "        </state-transition-element> "
                for j in range(1,length-dist):
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+((i%length-(length-dist)+j)*2-1)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                j = j+1
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+((i%length-(length-dist)+j)*2-1)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist)+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2+1)*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1

            elif i%length==dist:
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+((i%length-(length-dist))*2-1)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+1)*(length-dist)+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+2)*(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i+((i%length-(length-dist))*2)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+1)*(length-dist)+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+2)*(length-dist)+1)
                print "        </state-transition-element> "
                for j in range(1,length-dist):
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+((i%length-(length-dist)+j)*2-1)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                j = j+1
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+((i%length-(length-dist)+j)*2-1)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1

            elif i%length>1 and i%length<=(length-dist):

                if i%length==(length-dist):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(length-dist)*2+1)
                    print "        </state-transition-element> "
                    for j in range(1,length-dist):
                        print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                        print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+(2*j)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                    j=j+1
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1

                else:
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                    print "        </state-transition-element> "
                    for j in range(1,i):
                        print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                        print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*j*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                    j=j+1
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1

            else:
                #last rows with empty elements
                if i%length > dist:
                    for j in range(1, length-i%length+1):
                        #others
                        if j < (length-i%length):
                            print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*(dist-j)-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j))*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)+1)*(length-dist)+1)
                            print "        </state-transition-element> "
                            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+(2*(dist-j))*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j))*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)+1)*(length-dist)+1)
                            print "        </state-transition-element> "
                        #first two
                        else:
                            print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*(dist-j)-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+2)*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+3)*(length-dist)+1)
                            print "        </state-transition-element> "
                            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(dist-j)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+2)*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+3)*(length-dist)+1)
                            print "        </state-transition-element> "

                    #last two STE in the column
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*dist-1+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*dist*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+2*dist*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1
    if dist==length-1:
        for i in range(1,length+1):
            if i % length == 0:
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+101)
                print '                <activate-on-match element="%d"/>' %(start_id+101+length2-dist2)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*dist*(length-dist)),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+101)
                print '                <activate-on-match element="%d"/>' %(start_id+101+length2-dist2)
                print "        </state-transition-element> "

            elif i % length == (length-1):
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+2*(i-2)+1,character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+3)
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+4)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(i-2)+2),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+3)
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+4)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+2*(i-2)+3),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+5)
                print "        </state-transition-element> "
                i=i+1

            elif i%length==1:
                #not always all-input
                print '        <state-transition-element id="%d" symbol-set="[%s%s]" start="all-input">' %(start_id+i,character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+1+length-dist)
                print '                <activate-on-match element="%d"/>' %(start_id+i+(length-dist)*2+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]" start="all-input">' %((start_id+i+length-dist),character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+3*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1


            else:
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+2*(i-2)+1,character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+3)
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+4)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(i-2)+2),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+3)
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+4)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+2*(i-2)+3),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+3+2)
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+3+3)
                print "        </state-transition-element> "
                i=i+1



    if dist<0:
        print "Distance is at least 0!!!"

    return

def last(start_id, number_of_grna, length, dist, character_upper, character_lower):
    if dist>=2 and dist <= length/2:
        for i in range(1,length+1):
            if i%length == 1:
                #not all-input
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                print "        </state-transition-element> "

                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+length-dist,character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1+length-dist)
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1+length-dist+length-dist)
                print "        </state-transition-element> "
                i=i+1

            elif i%length==0:
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(300*number_of_grna)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*dist*(length-dist)),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(300*number_of_grna)
                print "        </state-transition-element> "

            elif i%length > dist and i%length < (length-dist):
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                print "        </state-transition-element> "
                for j in range(1,dist):
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+(2*j)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                j = j+1
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+(2*dist)*(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+(2*dist)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+(2*dist)*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1

            elif i%length>1 and i%length<=dist:

                if i%length==dist:
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                    print "        </state-transition-element> "
                    for j in range(1,dist):
                        print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                        print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+(2*j)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                    j=j+1
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*dist)*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1

                else:
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[0], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                    print "        </state-transition-element> "
                    for j in range(1,i):
                        print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                        print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*j*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                    j=j+1
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1

            else:
                #last rows with empty elements
                if i%length > length-dist:
                    ####should I +1 or not?
                    for j in range(1, length-i%length+1):
                        #others
                        if j < (length-i%length):
                            print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*(dist-j)-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j))*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)+1)*(length-dist)+1)
                            print "        </state-transition-element> "
                            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+(2*(dist-j))*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j))*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)+1)*(length-dist)+1)
                            print "        </state-transition-element> "
                        #first two
                        else:
                            print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*(dist-j)-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+2)*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+3)*(length-dist)+1)
                            print "        </state-transition-element> "
                            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(dist-j)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+2)*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+3)*(length-dist)+1)
                            print "        </state-transition-element> "

                    #last two STE in the column
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*dist-1+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*dist*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+2*dist*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1

                #last colum with full elements
                else:
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(length-dist)*2+1)
                    print "        </state-transition-element> "
                    for j in range(1,dist):
                        print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+2*j*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                        print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+ 2*j*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+ 2*j*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+ (2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "

                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+2*dist*(length-dist)+1)
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*dist*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+2*dist*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1

    if dist==1:
        for i in range(1,length+1):
            if i % length == 0:
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+length-dist),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(300*number_of_grna)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(length-dist)),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(300*number_of_grna)
                print "        </state-transition-element> "

            elif i % length == (length-1):
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1

            elif i%length==1:
                #not always all-input
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+length-dist),character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1


            else:
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1



    if dist==0:
        if i % length == 0:
            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[length-1], character_lower[length-1])
            print '                <activate-on-match element="%d"/>' %(300*number_of_grna)
            print "        </state-transition-element> "
        if i%length==1:
            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[0], character_lower[0])
            print '                <activate-on-match element="%d"/>' %(start_id+i+1)
            print "        </state-transition-element> "

        else:
            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
            print '                <activate-on-match element="%d"/>' %(start_id+i+1)
            print "        </state-transition-element> "
            i=i+1

    if dist > length/2 and dist < length-1:
        for i in range(1,length+1):
            if i%length == 1:
                print '        <state-transition-element id="%d" symbol-set="[%s%s]" start="all-input">' %(start_id+i,character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                print "        </state-transition-element> "

                print '        <state-transition-element id="%d" symbol-set="[^%s%s]" start="all-input">' %(start_id+i+length-dist,character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1+length-dist)
                print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1+length-dist+length-dist)
                print "        </state-transition-element> "
                i=i+1

            elif i%length==0:
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(300*number_of_grna)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*dist*(length-dist)),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(300*number_of_grna)
                print "        </state-transition-element> "

            elif i%length > (length-dist) and i%length < dist:
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+((i%length-(length-dist))*2-1)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+1)*(length-dist)+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+2)*(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i+((i%length-(length-dist))*2)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+1)*(length-dist)+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+2)*(length-dist)+1)
                print "        </state-transition-element> "
                for j in range(1,length-dist):
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+((i%length-(length-dist)+j)*2-1)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                j = j+1
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+((i%length-(length-dist)+j)*2-1)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist)+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2+1)*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1

            elif i%length==dist:
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+((i%length-(length-dist))*2-1)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+1)*(length-dist)+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+2)*(length-dist)+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i+((i%length-(length-dist))*2)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+1)*(length-dist)+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist))*2+2)*(length-dist)+1)
                print "        </state-transition-element> "
                for j in range(1,length-dist):
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+((i%length-(length-dist)+j)*2-1)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                j = j+1
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+((i%length-(length-dist)+j)*2-1)*(length-dist),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+((i%length-(length-dist)+j)*2)*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1

            elif i%length>1 and i%length<=(length-dist):

                if i%length==(length-dist):
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(length-dist)*2+1)
                    print "        </state-transition-element> "
                    for j in range(1,length-dist):
                        print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                        print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+(2*j)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                    j=j+1
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1

                else:
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id+i,character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+length-dist+1)
                    print "        </state-transition-element> "
                    for j in range(1,i):
                        print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                        print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*j*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                        print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                        print "        </state-transition-element> "
                    j=j+1
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*j-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j)*(length-dist)+1)
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*j+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1

            else:
                #last rows with empty elements
                if i%length > dist:
                    for j in range(1, length-i%length+1):
                        #others
                        if j < (length-i%length):
                            print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*(dist-j)-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j))*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)+1)*(length-dist)+1)
                            print "        </state-transition-element> "
                            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+(2*(dist-j))*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j))*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)+1)*(length-dist)+1)
                            print "        </state-transition-element> "
                        #first two
                        else:
                            print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*(dist-j)-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+2)*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+3)*(length-dist)+1)
                            print "        </state-transition-element> "
                            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(dist-j)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+2)*(length-dist)+1)
                            print '                <activate-on-match element="%d"/>' %(start_id+i+(2*(dist-j)-1+3)*(length-dist)+1)
                            print "        </state-transition-element> "

                    #last two STE in the column
                    print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+(2*dist-1+1)*(length-dist)+1)
                    print "        </state-transition-element> "
                    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*dist*(length-dist)),character_upper[i%length-1], character_lower[i%length-1])
                    print '                <activate-on-match element="%d"/>' %(start_id+i+2*dist*(length-dist)+1)
                    print "        </state-transition-element> "
                    i=i+1
    if dist==length-1:
        for i in range(1,length+1):
            if i % length == 0:
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+(2*dist-1)*(length-dist)),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(300*number_of_grna)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*dist*(length-dist)),character_upper[length-1], character_lower[length-1])
                print '                <activate-on-match element="%d"/>' %(300*number_of_grna)
                print "        </state-transition-element> "

            elif i % length == (length-1):
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+2*(i-2)+1,character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+3)
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+4)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(i-2)+2),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+3)
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+4)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+2*(i-2)+3),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+5)
                print "        </state-transition-element> "
                i=i+1

            elif i%length==1:
                #not always all-input
                print '        <state-transition-element id="%d" symbol-set="[%s%s]" start="all-input">' %(start_id+i,character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+1+length-dist)
                print '                <activate-on-match element="%d"/>' %(start_id+i+(length-dist)*2+1)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]" start="all-input">' %((start_id+i+length-dist),character_upper[0], character_lower[0])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(length-dist)+1)
                print '                <activate-on-match element="%d"/>' %(start_id+i+3*(length-dist)+1)
                print "        </state-transition-element> "
                i=i+1


            else:
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %(start_id+i+2*(i-2)+1,character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+3)
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+4)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %((start_id+i+2*(i-2)+2),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+3)
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+1+4)
                print "        </state-transition-element> "
                print '        <state-transition-element id="%d" symbol-set="[^%s%s]">' %((start_id+i+2*(i-2)+3),character_upper[i%length-1], character_lower[i%length-1])
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+3+2)
                print '                <activate-on-match element="%d"/>' %(start_id+i+2*(i-2)+3+3)
                print "        </state-transition-element> "
                i=i+1


    if dist<0:
        print "Distance is at least 0!!!"

    return

def pam(start_id, pam_upper, pam_lower):
    length = len(pam_upper)
    for i in range(length-2):
        if pam_upper[i] == 'N':
            print '        <state-transition-element id="%d" symbol-set="*">' %(start_id-i)
            print '                <activate-on-match element="%d"/>' %(start_id-i-1)
            print "        </state-transition-element> "
        else:
            print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id-i,pam_upper[i], pam_lower[i])
            print '                <activate-on-match element="%d"/>' %(start_id-i-1)
            print "        </state-transition-element> "


    print '        <state-transition-element id="%d" symbol-set="[%s%s]">' %(start_id-2,pam_upper[2], pam_lower[2])
    print '                <report-on-match/>'
    print "        </state-transition-element> "
    return

print'<?xml version="1.0" encoding="UTF-8"?>'
print'<automata-network id="mismatch1" name="mismatch1">'
print'        <description></description>'

with open(filename) as f:
    i=0
    for line in f:
        s = line
        character_upper=s.upper()
        character_lower=s.lower()
        start(i*300,8,12,dist1,dist2,character_upper[0:8],character_lower[0:8])
        last(i*300+100,(i+1),12,dist2,character_upper[8:20],character_lower[8:20])
        pam(300*(i+1),character_upper[20:], character_lower[20:])
        i=i+1

print '</automata-network>'
