from pywebio import *
from pywebio.output import *
from pywebio.input import *
import argparse
import pandas as pd 
from datetime import datetime
from pywebio import start_server
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import plotly.express as px 
import time
from functools import partial
import math 
import scipy.stats

def main():
    def counter(num):
        num += 1 
        counter.poot = num 

    def retardingButton():
        put_button("Re-enter Max Score", onclick=lambda: getMax(), color='success', outline=True)
    counter(-1)

    def returnElement(item):
        clear(None)
        put_markdown("You have selected [" + item + "] to do data analysis on!").style('color: blue; font-size: 20px')
        backButton()
        retardingButton() 
        put_markdown('____________________________________').style('color: blue; font-size: 20px')
        if counter.poot == 0:
            getMax()
            counter(1) 
        functions(item)

    def getMax():
        with use_scope("Scope2"):
            put_markdown("Enter the max score for this assignment down below: ")
        DOB = input("", placeholder = "Max Score (EX: 156)", required=False)
        getMax.getDOB = DOB
        clear('Scope2')
    
    def functions(item):
        put_markdown("Here are some things you can figure out with the entered test data: ")
        centralTendacies(item, 1) 
        compareLastYear(item)
        histogramgraph(item)
        boxPlot(item)
        put_markdown("-=-=- OUTPUT LINE -=-=-").style('color: red; font-size: 30px')


    def putButton(col):
        put_button(col, onclick=lambda: returnElement(col), color='success', outline=True)

    def putButtonOne(item):
        put_button("Reselect another analysis!", onclick=lambda: returnElement(item), color='success', outline=True)

    def markdown(df):  
        put_markdown('____________________________________').style('color: blue; font-size: 20px')
        put_markdown('Assignments you can do analysis on:')
        for col in df.columns:
            putButton(col) 
    
    def pretex():
        put_image('https://cdn.discordapp.com/attachments/689663355874443278/1014344505819930654/download.png', width = '300px', height = '120px')
        put_markdown('____________________________________').style('color: blue; font-size: 20px')
        put_markdown('This tool is used for math teachers to quickly get valuable data analysis of students\' test scores.').style('color: blue; font-size: 20px')
        userfile = file_upload("Select CSV File with your students\' test scores:", accept="text/csv", multiple=False)
        open(userfile['filename'], 'wb').write(userfile['content'])
        df = pd.read_csv(userfile['filename'])
        pretex.getFile = df
        markdown(df) 

    def cleanLean():
        clear(None)
        markdown(pretex.getFile)

    def backButton():
        put_button("Reselect from List", onclick=lambda: cleanLean(), color='success', outline=True)
    
    def returnCentralTendacies(item, conditions):
        df = pretex.getFile
        list = df[item]
        returnCentralTendacies.getSize = len(list)
        maxScore = int(float(getMax.getDOB)) 
        mean = 0 
        meanPercentage = 0 
        total = 0 
        for pitem in list:
            total += pitem
            mean = total / len(list)
            meanPercentage = (mean / maxScore) * 100 
        # put_markdown("Mean: " + str(mean) + " points or " + str(meanPercentage) + "%") 

        sortedList = df[item].sort_values()
        returnCentralTendacies.getSortedList = sortedList 
        a, aplus, aminus, b, bplus, bminus, c, cplus, cminus, d, dplus, dminus, f = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
        fullRange = [100, 93, 90, 87, 83, 80, 77, 73, 70, 67, 63, 60, 0]
        halfRange = [100, 90, 80, 70, 60, 0]

        for litem in sortedList:
            x = float(litem)
            if math.isnan(x):
                continue
            meanPercentages = int((litem / int(maxScore)) * 100)
            if meanPercentages >= 100:
                aplus += 1
            elif meanPercentages >= 93:
                a += 1
            elif meanPercentages >= 90:
                aminus += 1
            elif meanPercentages < 87:
                bplus += 1
            elif meanPercentages >= 83:
                b += 1
            elif meanPercentages >= 80:
                bminus += 1
            elif meanPercentages >= 77: 
                cplus += 1
            elif meanPercentages >= 73: 
                c += 1
            elif meanPercentages >= 70: 
                cminus += 1
            elif meanPercentage >= 67:
                dplus += 1
            elif meanPercentage >= 63:
                d += 1
            elif meanPercentage >= 60:
                dminus += 1
            elif meanPercentage >= 0:
                f += 1

        k = 0
        grades = [aplus, a, aminus, b, bplus, bminus, c, cplus, cminus, d, dplus, dminus, f]
        gradeString = ["A+", "A", "A-", "B", "B+", "B-", "C", "C+", "C-", "D", "D+", "D-", "F"]
        gradeStringSimple = ["A", "B", "C", "D", "F"] 
        added = 0 
        congested = []
        l = 0 

        def getMedian(job):
            if len(job) % 2 == 0:
                top = int((len(job) / 2)+ 1)
                bottom = int((len(job) / 2) - 1)
                median = (job[top] + job[bottom]) / 2
            else:
                median = job[(len(job) / 2) + 0.5]
            return median 
        
        for i in range(len(grades) - 1):
            added += grades[i]
            l += 1
            if l == 3:
                congested.append(added)
                l = 0 
                continue
            else:
                continue 
        congested.append(grades[len(grades) - 1])
        
        u = 0 
        for oitem in congested:
            if oitem > u:
                u = oitem
            else:
                continue

        for bitem in grades:
            if bitem > k:
                k = bitem
            else:
                continue
        
        if conditions == 1:
            put_markdown("Mean: " + str(mean) + " points or " + str(meanPercentage) + "%") 
            put_markdown("Mode: " + str(gradeString[grades.index(k)]))
            put_markdown("Mode without plus or minuses: " + str(gradeStringSimple[congested.index(u)])) 
            put_markdown("Median: " + str(getMedian(sortedList)) + " points or " + str((getMedian(sortedList) / maxScore) * 100) + "%") 
            putButtonOne(item)

        returnCentralTendacies.getMean = mean
        returnCentralTendacies.getMeanPercentage = meanPercentage
        returnCentralTendacies.getMode = str(gradeString[grades.index(k)]) 
        returnCentralTendacies.getModeWithout = str(gradeStringSimple[congested.index(u)])
        returnCentralTendacies.getMedian = getMedian(sortedList) 
        returnCentralTendacies.getMedianPercentage = (getMedian(sortedList) / maxScore) * 100 

    def centralTendacies(item, condition):
        put_button("Central Tendacies", onclick=lambda: returnCentralTendacies(item, condition), color='danger', outline=True)

    def returnCompareLastYear(item): 
        returnCentralTendacies(item, 0)
        meanDiff = returnCentralTendacies.getMean - 129.1875 
        medianDiff = returnCentralTendacies.getMedian - 134.5 
        put_markdown("If the number is negative, it means that score is lower than last year!").style('color: gray')
        put_markdown("Difference in mean: " + str(meanDiff) + " points")
        put_markdown("Difference in Mode: " + "Last year Mode is B+, while this year is " + returnCentralTendacies.getMode )
        put_markdown("Difference in Mode without plus or minuses: " + "Last year Mode is B, while this year is " + returnCentralTendacies.getModeWithout)
        put_markdown("Difference in Median: "  + str(medianDiff) + " points")
        sigTesting(item) 
        putButtonOne(item)
        

    def compareLastYear(item):
        put_button("Compare to Last Year", onclick=lambda: returnCompareLastYear(item), color='danger', outline=True)

    def returnSigTesting(item): 
        put_markdown("-=-=-=- Significance Testing Ouput Line -=-=-=-").style('color=red')
        maxes = int(float(getMax.getDOB)) 
        hNot = float(129.1875  / maxes)
        hAlt = float(returnCentralTendacies.getMean / maxes) 
        def getZ(alt, nott):
            numerator = float(alt - nott) 
            denominator = float(math.sqrt(nott * (float(1)-nott))) / float(returnCentralTendacies.getSize) 
            z = numerator / denominator
            return z 
        
        z = getZ(hAlt, hNot)
        pValue = scipy.stats.norm.sf(abs(z))
        if (hNot > hAlt): #scored worse than last year
            if pValue < 0.05:
                put_markdown("It is statistically significant that the class scored worse than last year: " + str(pValue) + " < 0.05 ")
            else:
                put_markdown("It is not statistically significant that the class did worse than last year. Class of 2023 did worse most likely due to chance.")
        if (hNot < hAlt): #scored better than last year
            if pValue < 0.05:
                put_markdown("It is statistically significant that the class scored worse than last year: " + str(pValue) + " < 0.05 ")
            else:
                put_markdown("It is not statistically significant that the class did better than last year. Class of 2023 did better most likely due to chance. ")        
        if (hNot == hAlt): #scored exactly the sam        
            put_markdown("Scored exactly the same (6-7 decimal places)")
            put_markdown(str(pValue))
        
    
    def sigTesting(item):
        put_button("Significance Testing (Mean)", onclick=lambda: returnSigTesting(item), color='danger', outline=True)

    def returnHistogramGraph(item):
        returnCentralTendacies(item, 0)
        group = [] 
        group = returnCentralTendacies.getSortedList
        fig = px.histogram(group, nbins=18)
        fig_html = fig.to_html(include_plotlyjs='require')
        put_html(fig_html)
        if returnCentralTendacies.getMean > returnCentralTendacies.getMedian:
            put_text("Score is right skewed. Not good!").style('color: red')
        else:
            put_text("Score is left skewed. Good!").style('color: green')
        putButtonOne(item) 

    def histogramgraph(item):
        put_button("Generate Histogram", onclick=lambda: returnHistogramGraph(item), color='danger', outline=True)
    
    def returnBoxPlot(item):
        returnCentralTendacies(item, 0)
        group = [] 
        group = returnCentralTendacies.getSortedList
        fig = px.box(group)
        fig_html = fig.to_html(include_plotlyjs='require')
        put_html(fig_html)   
        
        putButtonOne(item)


    def boxPlot(item):
        put_button("Generate Boxplot", onclick=lambda: returnBoxPlot(item), color='danger', outline=True)
    pretex()




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=8080)
    args = parser.parse_args()
    
    start_server(main, port=args.port)
    # start_server(main, port=8888, debug=True)

