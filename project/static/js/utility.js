
/*
 * $Id: utility.js 52 2014-06-02 15:08:53Z ryao $
 *
 * Copyright (c) 2013 - The University of Texas MD Anderson Cancer Center
 *
 * Depends on jquery
 *
 */
 
//utility function to process query string

(function($) {

    var debug = false;
	
    $.QueryString = (function(a) {
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i)
        {
            var p=a[i].split('=');
            if (p.length != 2) continue;
            b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
    })(window.location.search.substr(1).split('&'))
    
    $.intersect = (function (lista, listb) {
	    var intersectionElement = lista.concat(listb).filter(function(val,idx,arr){return arr.indexOf(val) !== idx;});
	    return intersectionElement;
    });
    $.uniqueValue = (function (a){
        return a.filter(function (value, index, self) {return self.indexOf(value) === index;});
    });   
    //check if element in mySymbolList falls between start and end in a selected Chromosome 
    $.captureSymbols = (function (start,end, mySymbolList, selectedChrom){
        if (debug) console.log("captureSymbols: start="+start+" end="+end);
        if (debug) console.log("captureSymbols: selected chromosome "+selectedChrom)
        var symbols = []; 
        var geneStart;
        mySymbolList.forEach(function (d){
            if ( d.geneSmashInfo.Maps !== undefined ) { 
                var len = d.geneSmashInfo.Maps.length;
                if (d.geneSmashInfo.Maps[len-1] !== undefined)
                    geneStart = d.geneSmashInfo.Maps[len-1].TranscriptionStart; 
            }
            if (d.geneSmashInfo.TranscriptionStart !== undefined) {
                geneStart = d.geneSmashInfo.TranscriptionStart
            }
            if ( $.convertToRow(d.geneSmashInfo.Chromosome) === selectedChrom.originalRowId){
                if (start<= geneStart && geneStart <= end ){
                    if (debug) console.log("pushed ............. "+d.geneSmashInfo.Symbol)
					//if type is mir, record symbol as miRbase
					if (d.geneSmashInfo.miRbase !== undefined)
						symbols.push(d.geneSmashInfo.miRbase);
					else
						symbols.push(d.geneSmashInfo.Symbol);
                }
            }
        })
        return symbols;
    }) //end of captureSymbols

    //convert chromosome to an integer row id for drawing purpose;
    //val can be chr1, chrX ... or just 1, 2,...,22, X
    $.convertToRow = (function (val) { 
        var chr;	
        if (val.length > 2) {
            chr = val.substring(3);
        }
        else {
            chr = val;
        }
        if (chr == "X" | chr == "x") return(23);
        else if (chr == "Y" | chr == "y") return(24);
		
        chr = parseInt(chr);
        //catch any invalid chromosome number
        if (chr <=0 | chr > 22) {
            return NaN;
        }
        else 
            return chr;
    });
   
    //check if it is a valid human chromosome
    $.isValidChromosome = (function (chr) {
		
        if (chr == "X" | chr =="x" | chr == "Y" | chr == "y") 
            return true;
                    
        if (parseInt(chr)){
            if (chr <=0 | chr > 22) {
                return false;
            }
            return true;
        }
        else {
            return false;
        }
    });
    
    //to test if aName in nameArr
    $.findName = (function (aName, nameArr) {  
        if (nameArr)
            return nameArr.indexOf(aName) != -1;
    })
    
    //for a given gene transcription start and end point, want to see its neighbour
    //by simply add factor more at the start point and more at the end point
    $.expandNeighbor = (function (start, end, factor) {
        var length = end - start;
        var result = {};
		return {start: Math.round(+start - +length*factor), end: Math.round(+end + +length*factor)}   
    });
    
    $.createColorMap = (function (colorArr) {
        var colorMap = [];
        colorMap["gpos100"] = colorArr[0];
        colorMap["gpos75"] = colorArr[1];
        colorMap["gpos50"] = colorArr[2];
        colorMap["gpos25"] = colorArr[3];
        colorMap["gneg"] = colorArr[4];
        colorMap["acen"] = colorArr[5];
        colorMap["gvar"] = colorArr[6];
        colorMap["stalk"] = colorArr[7];
        return(colorMap)
    });
    
    //find if a str name is in the chromosome array
    //return index of the chromosome array if found, otherwise return -1
    $.chromosomeIndex = (function (chrArr, str) {
        for (var i= 0; i < chrArr.length; i++){
            if (chrArr[i].name === str) return(i);
        }
        return -1;
    });
})(jQuery);
