/*
 * $Id: ideogram.js 57 2014-06-09 16:28:15Z ryao $
 *
 * Copyright (c) 2014 - The University of Texas MD Anderson Cancer Center
 *
 * Depends on d3
 */

var Ideogram = (function() {
    
    //global variables 
    var xscale, xscale_copy;
    var yscale;
    //yscaleForRect is the fraction of rectangle height    
    var yscaleForRect = 0.5; 
    var svg;
    var chrPanel;
	var sideChrPanel;
	var sideChr;
	var chr, cytoband;
	var pathP, pathQ;
    var selector;
	var geneLine, geneLabel;
    
    //data structure of chromosome array, for 24 human chromosome, array length is 23 
    //each chromosome is an object, contains fields
    //name: chromosome name
    //rowid: a row id for drawing on the canvas
    //originalRowid: according to human chromosome naming, 1-22, and x is 23, y is 24
    //cytoband array: each cytoband has fields: start, end, label, rowid, color
    //centromere p arm:  an object with fields: start, end, label, rowid, color
    //centromere q arm:  an object with fields: start, end, label, rowid, color
    var chromosomeArr =[];
    var displayChromArr = [];
    
    //default zoom factor
    var zoomFactor = 32;
    var myzoom;
    var interGenelist=null;
    var interMirlist=null;
	var chromlist=null;
    var currentStateIsSelection = false;
  
    //color map use to draw the color of each cytoband
    //from cytobands color in R package, refer to http://www.bioconductor.org/packages/2.11/bioc/vignettes/biovizBase/inst/doc/intro.pdf
    //R colors, refer to http://www.stat.columbia.edu/~tzheng/files/Rcolor.pdf
    //javascript d3 named color , refer to http://www.w3.org/TR/SVG/types.html#ColorKeywords
    // this is the color from R package biovizBase
    //var colorArr = ["#000000", "#404040", "#808080", "#C1C1C1", "grey100", "brown4", "grey0", "brown3" ];
    // this is the color from R converted to d3 named color
    var colorArr = ["black", "grey", "lightslategrey", "lightgrey", "whitesmoke", "brown", "black", "firebrick" ];
    var myColorMap = $.createColorMap(colorArr);   
    //array of input gene/mirRNAID to display on the ideogram
    var geneArr = []; 
    var oncogeneData =[];
    var suppressorData=[];
    var oncogeneDataCopy=[];
    var suppressorDataCopy=[];
    var cancerGeneArr =[];
    var mySymbolList = [];
    // an array of genes fail to retrieve annotation from geneSmash
    var excludedGenes =[];  
    var margin = {
        top: 0, 
        right: 20, 
        bottom: 30, 
        left: 100
    };
    var plotGeometry = {         
        plotWidth:    1000,
        plotHeight:   1000,
        sideChrWidth: 100
    }
    var totalHumanChromosome = 24;
    var spaceBetweenChromosome=0;
    var horizontalShift = margin.left+10 
    //select a genomic fragment
    var mousedownX;
    var svgrect, selectedYpos, selectedChrom;
    var selectedGenomeStart, selectedGenomeEnd, selectionBox;
    //functions
    var geneClick,brushClick, hideMenu;
    //data collected from geneSmash
    var geneData=[];
    
	var debug = false;
	
    // Constructor function for Ideogram object 
    function IdeogramObj (chromosomeArr ) {
        this.chromosomeArr = chromosomeArr;
    };
    IdeogramObj.prototype.IdeogramPlot = IdeogramPlot;
    IdeogramObj.prototype.zoomIn = zoomIn;
    IdeogramObj.prototype.zoomOut = zoomOut;
    IdeogramObj.prototype.resetScale = resetScale;
    IdeogramObj.prototype.reactivateZoom = reactivateZoom;
    IdeogramObj.prototype.removeSelectionBox = removeSelectionBox;
    IdeogramObj.prototype.removeOncogene = removeOncogene;
    IdeogramObj.prototype.removeSuppressor = removeSuppressor;
    IdeogramObj.prototype.redraw = redraw;
    IdeogramObj.prototype.resizePlot = resizePlot;
    

    function createIdeogram (cytobandFileUrl, callback){
        chromosomeArr = []; //initialize the chromosomeArr before Ideogram object is creatated
        d3.tsv (cytobandFileUrl , function(error, graphInputData) {
            
            graphInputData.forEach(function(d) 
            { 
                //input file order from chr1, chr10, chr11, 
                //but we need the order chr1, chr2 ... chrX, chrY to store 
                //so rowid 1 for chr1, 2 for chr2 ... 23 for chrX, 24 for chrY
                var rowid = $.convertToRow(d.chr);
              
                //add chromosome to chromosome array if not seen before
                var chrIdx = $.chromosomeIndex (chromosomeArr, d.chr);
                if (chrIdx === -1) {              
                    //We haven't seen this chromosome before, create a new chromosome entry
                    var newChromosome = {
                        name: d.chr,
                        rowid: rowid,
                        originalRowId: rowid,
                        cytobands: [],
                        pArm: undefined,
                        qArm: undefined
                    }; 
                
                    chromosomeArr.push(newChromosome);
                    chrIdx = chromosomeArr.length -1;
                }
               
                function createCytobandOrCentromereObj (d) {
                    var newObj = {
                        start: +d.start,
                        end:   +d.end,
                        label: d.cytoband,
                        rowid: rowid,
                        color: d.color
                    }
                    return newObj;
                }
               
                //process row information and store to the cytoband array            
                //if it's not a centromere arm
                if (d.color != "acen") {
                    var cytobandArrIdx = chromosomeArr[chrIdx].cytobands.length;
                    chromosomeArr[chrIdx].cytobands[cytobandArrIdx] = createCytobandOrCentromereObj(d);
                }
                //process centromere
                else {
                    //see p arm in a chromosome, create pArm object
                    if (chromosomeArr[chrIdx].pArm === undefined) {
                        chromosomeArr[chrIdx].pArm = createCytobandOrCentromereObj(d);
                    }
                    //have seen p arm in a chromosome, process q arm in the same chromosome, create qArm object
                    else {
                        chromosomeArr[chrIdx].qArm = createCytobandOrCentromereObj(d);
                    }                
                }
            })
            //use rowid to sort array, so chr1, chr2, chr3 ... in order (originally the input file has chr1, chr10, chr11 ... chrX, chrY in order)
            chromosomeArr.sort(function(a,b){
                return a.rowid-b.rowid
            });
            //console.log(chromosomeArr)   
            callback (new IdeogramObj (chromosomeArr));
        }) //end of d3.tsv
    }
    
    function IdeogramPlot (refUrlAPI, oncogeneData, suppressorData, mySymbolList, paramlist, selector, chromlist, geneClickFunc, brushClickFunc, hideMenuFunc, newW, newH)
    {   
        this.refUrlAPI = refUrlAPI;
        
        oncogeneData = oncogeneData;
        suppressorData = suppressorData;
        this.mySymbolListFromParam = mySymbolList;  //symbols (gene/mirRNAid from parameters)
        
        interGenelist = paramlist[6];
        interMirlist = paramlist[8];
        chromlist = chromlist;
      
        geneClick = geneClickFunc;
        brushClick = brushClickFunc;
        hideMenu = hideMenuFunc;
        
        //if input chromosome list in not null, update displayChromArr, then the chromosomeArr
        //to have the chromosomes to be displayed.
        if (chromlist) {
            chromlist.sort(function(a,b) {
                return $.convertToRow(a) - $.convertToRow(b)
            });
          
            displayChromArr = processDisplayChromosomes (chromlist, chromosomeArr);           
        }       
        //if displayChromArr gets updated by chromlist, which is not empty now
        if (displayChromArr.length >0) {
            //chromosomeArr always contains the data (chromosomes) to be drawn on the canvas
            chromosomeArr = displayChromArr;
        }  
     
        //plot ideogram chromosomes with cytobands on canvas once    
		makePlot(newW, newH, selector);
        
        //process cancer genes once and stored data in oncogeneDataCopy and suppressorDataCopy
        oncogeneDataCopy = processCancerGene(oncogeneData);
        suppressorDataCopy = processCancerGene(suppressorData);        
        
        //process geneSmash service call
        var len = this.mySymbolListFromParam.length;
        if (len> 0) {
            
            //if a symbol from parameter list is also an oncogene or suppressor, remove it from 
            //oncogeneDataCopy and suppressorDataCopy, so it won't overlap drawn
            //mark this genelabel to be "oncogenelabel" or "suppressorlabel"
			//if a symbol or ID from parameter list appears in interGenelist or interMirlist
			//remove one with class "gene2" or "mir2"
			//to avoid to be drawn twice
        
            if (interGenelist !== null || interMirlist !== null) {
                updateParamList(this.mySymbolListFromParam);
            }
            
            var updatelen = this.mySymbolListFromParam.length;
           
            if (updatelen <= len) {
                updateCancergeneCopyData(this.mySymbolListFromParam);
            }
            processHttpCall (this.refUrlAPI, this.mySymbolListFromParam);
        }
    }
    
	function makePlot(newW, newH, selector){
		if (!selector) {
            //console.warn('no target specified, defaulting to div.ideogramContent');
			selector = defaultSelector;
        }   
		
		var startMin = d3.min (chromosomeArr, function(x) {
            return d3.min(x.cytobands, function(cytoband) {
                return cytoband["start"];
            });
        });
        var endMax   = d3.max (chromosomeArr, function(x) {
            return d3.max(x.cytobands, function(cytoband) {
                return cytoband["end"];
            });
        });
		
		xscale = d3.scale.linear()
		.domain       ([startMin, endMax]); 
		
		yscale = d3.scale.linear()
		.domain       ([0, totalHumanChromosome]);
		
		myzoom= d3.behavior.zoom()
        .scaleExtent([1, zoomFactor])
		.on("zoom", function () {
				redraw ();
			});
		
		svg = d3.select(selector)
        .append("svg")
        .attr("id", "plotarea")
		.attr("pointer-events", "all")
		
		//-------------------------------------------
        //create ChromsomePanel on the svg canvas
        //--------------------------
		chrPanel = svg.append("svg:svg")
        .attr("id", "chrPanel")
		.attr("x", margin.left)
        .attr("y", margin.top );
		
		//background for chromosome template
        chrPanel.append("g")
        .attr("id", "background");
        //foreground for gene annotation line	
        chrPanel.append("g")
        .attr("id", "foreground");   
		
		var sideChrLabelxLevel = margin.left - 90; 
        //--------------------------------
        //create chromosome labels for side
        //----------------------------------                   
        sideChrPanel = svg.append("svg:svg")
        .attr("id", "sideChrLabel")
        .attr("x", sideChrLabelxLevel)
        .attr("y", margin.top);
		
		var displayLabelData = chromosomeArr.map(function(x) {
            return x.name;
        })
		
		sideChr = sideChrPanel.selectAll("text")
        .data(displayLabelData);
		sideChr.enter().append("svg:text")
        .attr("class", "label")
		 .text(function(d) {
            return (d);
        })
        .on("click", function (d) {
            labelClick (d);
        })
		
		//----------------------------------------------
        //cytobands
        //----------------------------------------------
		var displayChromosomeData = chromosomeArr;
        chr = chrPanel.selectAll("#background").selectAll("g.chromosome")
		.data(displayChromosomeData);
				 
        chr.enter().append("g")
        .attr("class", "chromosome");
		
		cytoband =chr.selectAll("rect.cytoband")
        .data( function(x) {
            return x.cytobands;
        });
              
        cytoband.enter().append("svg:rect")		
        .attr("class", "cytoband")
        .attr("fill",  function(d) {
            return myColorMap[d.color];
        })
        .append("svg:title")
        .text(function(d) { 
            return "cytoband: "+d.label+", "+d.start+" - "+d.end;
        });	
			
  
		//----------------------------------------------
        //pathP
        //----------------------------------------------
		pathP =chr.selectAll("path.centromereP")
        .data(function(x) {
            return [x.pArm];
        });
				
        pathP.enter().append("svg:path")
        .attr("class", "centromereP");
		
		//----------------------------------------------
        //pathQ
        //----------------------------------------------
		pathQ =chr.selectAll("path.centromereQ")
        .data(function(x) {
            return [x.qArm];
        })	
			
        pathQ.enter().append("svg:path")
        .attr("class", "centromereQ")
		
		resizePlot(newW, newH);
	}
	
    function resizePlot(newW, newH){
      
        if (newH)
            plotGeometry.plotHeight = newH;
        if (newW)
            plotGeometry.plotWidth = newW;
        
        spaceBetweenChromosome = plotGeometry.plotHeight/(totalHumanChromosome);
             
        //adjust chromosome panel's height
        var chrHeight = plotGeometry.plotHeight-margin.bottom ;
        
		//updates dimension based on newW and newH ...
		xscale
		.range        ([0, plotGeometry.plotWidth - plotGeometry.sideChrWidth]);
		
		yscale
		.range        ([0, chrHeight]);
		
		myzoom
		.x(xscale)   //horizontal zoom in/out
        
		svg
		.attr("width",  plotGeometry.plotWidth )
		.attr("height", plotGeometry.plotHeight )
		.call(myzoom) ;
       
        chrPanel
		.attr("width",  plotGeometry.plotWidth - plotGeometry.sideChrWidth )
        .attr("height", plotGeometry.plotHeight)
		  
        sideChrPanel 
        .attr("width", plotGeometry.sideChrWidth)
        .attr("height",  plotGeometry.plotHeight);	
				
        redraw();  //first time redraw(), no cancer gene involved, no flag parameters pass in
        
    } //end of function resizePlot();		
   
    function redraw(oncogeneflag, suppressorflag) {
        
        //decide cancer genes to be drawn based on input flags
        if (oncogeneflag!== undefined && suppressorflag !== undefined){
            if (oncogeneflag){
                oncogeneData = oncogeneDataCopy;
                if (suppressorflag){
                    suppressorData = suppressorDataCopy;
                    cancerGeneArr= oncogeneDataCopy.concat(suppressorDataCopy);
                }
                else 
                    cancerGeneArr= oncogeneDataCopy;
            }
            else {
                if (suppressorflag){
                    suppressorData = suppressorDataCopy;
                    cancerGeneArr= suppressorDataCopy;
                }
                else{
                    suppressorData=[];
                    oncogeneData=[];
                    cancerGeneArr=[];
                }
            }
        }
		
        sideChr
		.attr("y", function(d, ix) {
            return (yscale(ix+1) + yscale(yscaleForRect)) ;
        })
		
		sideChr.exit().remove(); 
		
        cytoband
		.attr("height", yscale(yscaleForRect))
        .attr("y", function(d) { 
            return yscale(d.rowid);
        } )
		//horizontal rescale
        cytoband.attr("x", function(d ) {
            return xscale(d.start);
        } )
        .attr("width", function(d) {
            var w= xscale(d.end) - xscale(d.start);
            return w;
        });
		
        cytoband.exit().remove();
	
        //--------------------------------------------
        // selecting a genomic fragment
        //--------------------------------------------          
        //make a copy of the xscale
        //xscale domain changes when mouse move and mouse up; use a copy of xscale for reverse function
        xscale_copy = xscale.copy();
        
        //mousemove on every chromosome, where has the data
        svg.select("#background").selectAll("g").on("mousemove", function(){  
            //change cursor style to haircross if ready for a selection
            if(d3.event.shiftKey){
                this.style.cursor="crosshair"; 
            } 
            else {
                this.style.cursor="default";
            }
        })
        //mousedown on a chromosome       
        svg.select("#background").selectAll("g").on("mousedown", function(d){
            mouseDownOnAChromosome(this, d);  //pass this svg element and chromosome d as parameters
        });
        
        //--------------------------------------------
        //draw chromosome centromere p arm
        //--------------------------------------------
        function makePpathString(d) {
				
            var x0 = xscale(d.start);
            var y0 = yscale(d.rowid);
            var x2 = xscale(d.end);
            var y2 = y0+ 1/2*yscale(yscaleForRect);
            var x4 = xscale(d.start);
            var y4 = y2+ 1/2*yscale(yscaleForRect);
            var x1 = x0+(x2-x0)*0.75;
            var y1 = y0;
            var x3 = x1;
            var y3 = y4;
               
            return ("M "+x0+" "+y0+" L "+x1+" "+y1+" L "+x2+" "+y2+" L "+x3+" "+y3+" L "+x4+" "+y4);			
        }
		
        //rescale p arm 
        pathP.attr("d", makePpathString);	
        pathP.exit().remove(); 	
			
        //--------------------------------------------
        //draw chromosome centromere q arm
        //--------------------------------------------
        function makeQpathString (d) {
            var x0 = xscale(d.end);
            var y0 = yscale(d.rowid);
            var x2 = xscale(d.start);
            var y2 = y0 + 1/2*yscale(yscaleForRect);
            var x4 = xscale(d.end);
            var y4 = y2+ 1/2*yscale(yscaleForRect);
            var x1 = x0-(x0-x2)*0.75;
            var y1 = y0;
            var x3 = x1;
            var y3 = y4;
            return ("M "+x0+" "+y0+" L "+x1+" "+y1+" L "+x2+" "+y2+" L "+x3+" "+y3+" L "+x4+" "+y4);
        }
            
		// rescale q arm	
        pathQ.attr("d", makeQpathString);
        pathQ.exit().remove(); 
			
        chr.exit().remove();
		
		drawSymbol();		
    } //end of redraw()	
    
	function drawSymbol(){
		
        //to include cancer genes as well
        var myDataArr1 = geneArr.concat(cancerGeneArr);
		var myDataArr = processSymbolListForDisplay(myDataArr1);
		
        geneLine= chrPanel.selectAll("#foreground").selectAll("line")
		.data(myDataArr);
   
        //----------------------------
        //draw gene on the chromosome
        //----------------------------	
        geneLine.enter().append("svg:line")	
        .on("mouseout", function(){d3.select(this).style("stroke-width", "2px");})
        //clickable gene
        .on('click' , function (d) {
            if (geneClick) {
                // 1.5 x for the genome location
                var zoomOutFactor = 0.25;
                var result;
                if (d.geneSmashInfo.Maps !== undefined ) { 
                    len = d.geneSmashInfo.Maps.length;
                    if (d.geneSmashInfo.Maps[len-1] !== undefined){
                        result = $.expandNeighbor (d.geneSmashInfo.Maps[len-1].TranscriptionStart,d.geneSmashInfo.Maps[len-1].TranscriptionEnd, zoomOutFactor );
                    }
                }
                if (d.geneSmashInfo.TranscriptionStart !== undefined) {
                    result = $.expandNeighbor (d.geneSmashInfo.TranscriptionStart,d.geneSmashInfo.TranscriptionEnd, zoomOutFactor );                 
                }
				//pass gene menu width and height
				var pos = adjustMenuPosition($('#geneMenu.menu').width(), $('#geneMenu.menu').height());
                geneClick (d.queryBy, d.geneSmashInfo._id, d.geneSmashInfo.Symbol, d.geneSmashInfo.miRbase, d.geneSmashInfo.Chromosome, result, pos);               
            }
        })
		
		//----------------------------------
		//draw geneLabel
		//----------------------------------
		geneLabel = chrPanel.selectAll("#foreground").selectAll("text")
        .data(myDataArr);
		geneLabel.enter().append("svg:text") 
        .on("click", function(d){
            if (geneClick) {
                // 1.5 x for the genome location
                var zoomOutFactor = 0.25;
                var result;
                if (d.geneSmashInfo.Maps !== undefined ) { 
                    len = d.geneSmashInfo.Maps.length;
                    if (d.geneSmashInfo.Maps[len-1] !== undefined){
                        result = $.expandNeighbor (d.geneSmashInfo.Maps[len-1].TranscriptionStart,d.geneSmashInfo.Maps[len-1].TranscriptionEnd, zoomOutFactor );
                    }
                }
                if (d.geneSmashInfo.TranscriptionStart !== undefined) {
                    result = $.expandNeighbor (d.geneSmashInfo.TranscriptionStart,d.geneSmashInfo.TranscriptionEnd, zoomOutFactor );                 
                }
				var pos = adjustMenuPosition($('#geneMenu.menu').width(), $('#geneMenu.menu').height());			
                geneClick (d.queryBy, d.geneSmashInfo._id, d.geneSmashInfo.Symbol, d.geneSmashInfo.miRbase, d.geneSmashInfo.Chromosome, result, pos);               
            }
        });
		
		redrawSymbol();
	}
	
	function redrawSymbol () {
	 
        var len;
        var spacer = 8; 
        	
        function myx(d) {      
           
            if (d.classtype !== undefined) {
                if (loadFromCancerGene(d) ){
                    if (d.geneSmashInfo.TranscriptionStart !== undefined)
                        return xscale(d.geneSmashInfo.TranscriptionStart);                 
                }   
                else {
                    if (d.geneSmashInfo.Maps !== undefined ) { 
                        len = d.geneSmashInfo.Maps.length;
                        if (d.geneSmashInfo.Maps[len-1] !== undefined)
                            return calculateX(d.geneSmashInfo) ;
                    }
                }
            } 
            //workout: let it out of the screen
            return -200;
        }
        
        //rescale geneLine
        geneLine
		.attr("class", function(d){
            return d.classtype;
        })	
        .attr("x1", function(d) {
            return myx(d);
        })
        .attr("y1", function(d) {
            return yscale(d.displayRowid) - spacer;
        })         
        .attr("x2", function(d) {
            return myx(d);
        })
        .attr("y2", function(d) {
            return yscale(d.displayRowid)+yscale(yscaleForRect)+spacer;
        }) 
		.on("mouseover", function(d){
			d3.select(this).style("stroke-width", "4px")
			if (d.display >0) {
				if (d.extraInfo !== undefined) 	{
					d3.select(this).style("stroke-width", "4px")			
					.append("svg:title")
					.text ( function(d) {
						return ("Found Nearby Symbols: "+d.extraInfo+"\nClick to show more options.\n"+d.geneSmashInfo.Symbol+": Entrez Id "+d.geneSmashInfo._id+"; "+d.geneSmashInfo.Description+"; GeneBank Ref "+d.geneSmashInfo.GenBank);
					})
				}
				else {
						d3.select(this).style("stroke-width", "4px")			
						.append("svg:title")
						.text ( function(d) {
							return ("Click to show more options.\n"+d.geneSmashInfo.Symbol+": Entrez Id "+d.geneSmashInfo._id+"; "+d.geneSmashInfo.Description+"; GeneBank Ref "+d.geneSmashInfo.GenBank);
						})
				}
			}
			else {
					d3.select(this).style("stroke-width", "4px")			
					.append("svg:title")
					.text( function (d) {
						return ("Click to show more options.\n"+d.geneSmashInfo.Symbol+": Entrez Id "+d.geneSmashInfo._id+"; "+d.geneSmashInfo.Description+"; GeneBank Ref "+d.geneSmashInfo.GenBank);
					})
			}
			
		})
		
        geneLine.exit().remove();
		
	    //---------draw geneLabel----------------
          
        var spacer = 2; 
        var spacer2= 3;
             
        // rescale gene labels
        geneLabel
		.attr("class", function(d){
            if (d.labeltype !== undefined ) return d.labeltype;
            else return "genelabel";            
        })
        .on("mouseover", function(d) {
            d3.select(this).style("font-weight", "bold").style("font-size", "14px");		
			if (d.extraInfo !== undefined) {
				d3.select(this).append("svg:title")
				.text( "Found Nearby Symbols: "+d.extraInfo+"\nClick to show more options.\n"+d.geneSmashInfo.Symbol+": Entrez Id "+d.geneSmashInfo._id+"; "+d.geneSmashInfo.Description+"; GeneBank Ref "+d.geneSmashInfo.GenBank);
			}
			else {
				d3.select(this).append("svg:title")
				.text( "Click to show more options.\n"+d.geneSmashInfo.Symbol+": Entrez Id "+d.geneSmashInfo._id+"; "+d.geneSmashInfo.Description+"; GeneBank Ref "+d.geneSmashInfo.GenBank);
			}
		})
        .on("mouseout", function() {
            d3.select(this).style("font-weight", "normal").style("font-size", "8px");
        })
        .attr("x", function(d) {
            if (d.geneSmashInfo.Maps !== undefined){
                return (calculateX(d.geneSmashInfo)+spacer2);
            }
            else 
                return (xscale(d.geneSmashInfo.TranscriptionStart)+spacer2);
        })
        .attr("y", function(d) {         
            return yscale(d.displayRowid) - spacer;
        })
        .text(function(d) {
            //if the gap between chromosome has enough space for displaying
            if (spaceBetweenChromosome >=20){
                if (d.display > 0)   
					//if multiple symbols are close together and can't show one at a time, append "+N";
					if (d.extraInfo !== undefined)
						return d.geneSmashInfo.Symbol+"+";
					else
						return d.geneSmashInfo.Symbol;
            }
        })
        
        geneLabel.exit().remove();
		
    } //end of redrawSymbol()
    
    function createMyGene (dataInfo, displayRowid) {
        //console.log(dataInfo)
        return {
            "geneSmashInfo": dataInfo,
            "displayRowid" : displayRowid
        }
    }
    function isInDisplayedChromosome(mySymbol, chromosomeArr){
       
        for (var i =0; i< chromosomeArr.length; i++){
            if (chromosomeArr[i].name.substring(3) === mySymbol.Chromosome) {
                return (chromosomeArr[i].rowid);   
            }
        };
        return 0;
    }
    function showExcludedGenes () {
		if (excludedGenes.length) {
			var geneStringNoAnno = excludedGenes.join(', ');	
			openDialogBox(geneStringNoAnno);
		}
    }//end of showExcludedGenes()
    function processHttpCall(refUrlAPI, genelist){
        
        //console.log("processhttpCall ...")
        var processGene =[] ;
        var displayRowid = 0;
        geneArr = [];   //to avoid redundant appending when check cancer gene box
        
        genelist.forEach (function(d){
            // d is not empty and not just whitespace
            if ( /\S/.test(d) ){
                processGene.push(d);
            }
        })
   
		
		processGene.forEach(function(d) {
			//geneSmash query by are specific for gene and microRNA Id
			var query;
				
			if (d.queryBy === "by_symbol") 
				query = refUrlAPI+d.queryBy+'?'+"key=\""+d.geneSmashInfo.Symbol+"\""+"&include_docs=true";			
	  
			if (d.queryBy === "by_mir")
				query = refUrlAPI+d.queryBy+'?'+"key=\""+d.geneSmashInfo.miRbase+"\""+"&include_docs=true";
				
			d3.json(query, ready);
				
			function ready(error, result){	
				if ( result.length > 0 ) {
					displayRowid = isInDisplayedChromosome(result[0],chromosomeArr);
					if (displayRowid >0 ) {
						geneArr.push (updateGeneFromGeneSmashService(d, result[0], displayRowid));
						drawSymbol();
					}
				}
				else {
					//does not receive gene annotation from geneSmash;	
					if (d.queryBy === "by_symbol") 
						excludedGenes.push(d.geneSmashInfo.Symbol);	
					if (d.queryBy === "by_mir")
						excludedGenes.push(d.geneSmashInfo.miRbase);
					showExcludedGenes();							
				}
			}
		}) //end of for forEach	
		
    } //end of function processHttpCall
    
    function updateMyGene(d, displayRowid){       
        d.displayRowid= displayRowid;  
        return d;
    }
    function updateGeneFromGeneSmashService(d, datainfo, displayRowid){ 
        d.geneSmashInfo = datainfo;
        d.displayRowid= displayRowid;  
        if ($.findName (d.geneSmashInfo.Symbol, interGenelist)) {
            d.classtype = "intergene";
        }       
        if ($.findName (d.geneSmashInfo.miRbase, interMirlist)) {
            d.classtype = "intermir";
        }
       
        return d;
    }

    function processCancerGene(geneData){
     
        var newGeneData =[];
        var displayRowid = 0;
        
        if (geneData) {                   
            geneData.forEach(function(d) {              
                
                displayRowid = isInDisplayedChromosome(d.geneSmashInfo,chromosomeArr);
                var updatedObj = updateMyGene(d, displayRowid);
                if (displayRowid >0 ) {
                    newGeneData.push(updatedObj);                                                      
                } 
            });          
        } 
        return newGeneData;
    }
    
    //-----------------------------------------
    // helper functions go here .... 
    //input: a chromosome list, an chromosome array
    //output: return displayChromArr contains only the chromosomes in the chromlist
    function processDisplayChromosomes (chromlist, chromArr) {
        
        displayChromArr = []; //initialize  
        chromlist.forEach (function (d) {
            if ( $.isValidChromosome(d)) { 
                var rowid = $.convertToRow(d);
                //retrieve data from chromArr[rowid-1] then rewrite rowid in displayChromArr
                var thisChrom = chromArr[rowid-1];
                thisChrom.rowid = displayChromArr.length+1;
                displayChromArr.push(thisChrom);
            }
            else{
                alert ("There was an error on this page.\n User input an invalid chromosome. \nInput a valid Chromosome: 1-22, X and Y.")
            }
        });
       
        //update the rowid for chromosome members
        displayChromArr.forEach (function (thisChrom){
            thisChrom.cytobands.forEach(function (d) {
                d.rowid = thisChrom.rowid;
            })
            thisChrom.pArm.rowid= thisChrom.rowid;
            thisChrom.qArm.rowid= thisChrom.rowid;
            
        });
        return displayChromArr;
    }
     
    function calculateX (d) {
        if (d.Maps !== undefined ) {
            var len = d.Maps.length;
            if (d.Maps[len-1] !== undefined)
                var geneStart = d.Maps[len-1].TranscriptionStart;
            return xscale(geneStart);
        }
        else {
            //workout: let it out of the screen
            return -200;
        }
    }
        
    function zoomIn(myZoomFactor){
      
        if (!currentStateIsSelection) {          
            var myscale = myzoom.scale();
            myzoom.scale(myZoomFactor*myscale);
            removeSelectionBox();
            hideMenu();
            redraw();        
        }
        else {
            console.log("In selection mode, zoom in/out inactivate")
        }
    }
        
    function zoomOut(myZoomFactor){
        if (!currentStateIsSelection) {
            var myscale = myzoom.scale();
            if (myscale > 1){
                myzoom.scale(myscale/myZoomFactor);
                removeSelectionBox();
                hideMenu();
                redraw();
            }
        }
        else {
            console.log("In selection mode, zoom in/out inactivate");
        }
    }
    function reset_xscale(){
        var startMin = d3.min (chromosomeArr, function(x) {
            return d3.min(x.cytobands, function(cytoband) {
                return cytoband["start"];
            });
        });
        var endMax   = d3.max (chromosomeArr, function(x) {
            return d3.max(x.cytobands, function(cytoband) {
                return cytoband["end"];
            });
        });
        xscale.domain([startMin, endMax]); 
    }
    function resetScale(){
            
        reset_xscale();
        myzoom
        .x(xscale)   //horizontal zoom in/out
        .on("zoom", function () {
            redraw ();
        });                        
        svg .call(myzoom);
        
        //resetScale also removes selectionbox and hide menu
        removeSelectionBox();
        removeGeneLabel();
        hideMenu();
        redraw();
    }       
    function reactivateZoom(){
        currentStateIsSelection = false;
        myzoom 
        .on("zoom", function () {
            redraw ();
        })   
        svg .call(myzoom);
    }
    function deactivateZoom(){ 
        currentStateIsSelection = true;
        myzoom.on('zoomstart',null).on('zoom',null).on('zoomend',null);
        svg.on("mousedown.zoom", null).on("onwheel.zoom", null).on("dblclick.zoom", null).on("touchstart.zoom", null);
    }
    function createSelectionBox(){  
        //create a single selectionBox on the foreground
        selectionBox =svg.selectAll("#foreground").selectAll("rect")
        .data([0]);           
        selectionBox.enter().append("svg:rect").attr("class", "selection");
    }
    function removeSelectionBox(){
        d3.select("body") .selectAll(".selection").remove();
        selectionBox = undefined;
    }
    function removeGeneLabel() {
        d3.select("body") .selectAll(".genelabel").remove(); 
        removeOncogeneLabel();
        removeSuppressorLabel();
    }
    function removeOncogeneLabel() {
        d3.select("body") .selectAll(".oncogenelabel").remove();       
    }
    function removeSuppressorLabel() {
        d3.select("body") .selectAll(".suppressorlabel").remove();       
    }
    function removeOncogene(selector) {
        //select selector instead of "body" to avoid removing any item from legend
        d3.select(selector) .selectAll(".oncogene").remove(); 
        oncogeneData =[];
        cancerGeneArr=suppressorData;
        removeOncogeneLabel();
    }
    function removeSuppressor(selector) {
        d3.select(selector) .selectAll(".suppressor").remove(); 
        suppressorData =[];
        cancerGeneArr=oncogeneData;  
        removeSuppressorLabel();        
    }
    function loadFromCancerGene(a){
  
        if (a.classtype === "oncogene" || a.classtype === "suppressor")
            return true;
        else
            return false
    }
    
    function selectionmove(mousedownX, svgrect){    
        d3.event.preventDefault();  
        d3.event.stopPropagation(); 
        var moveX = d3.event.clientX-horizontalShift;   //mouse move can be anywhere
        var x, width;
        
        if (moveX>=mousedownX ) {    //move to right 
            width = d3.min([(moveX-mousedownX+2), Math.abs(svgrect.width+svgrect.x-mousedownX+2)]);
            x = mousedownX;    
        }
        else {          //move to left 
            width = d3.min([(mousedownX-moveX), mousedownX-svgrect.x]); 
            x =  d3.max([moveX, svgrect.x]);
        }
        selectionBox.attr("x", x).attr("width", width);
    }
    function mouseup(selectedGenomeStart, selectedChrom){
        d3.event.preventDefault();  //with preventDefault, the window never sees the mouseup event
        d3.event.stopPropagation(); 
        //inactivate mousemove on svg; inactivate mouseup on body
        svg.on("mousemove", null);    
        d3.select("body").on("mouseup", null);
		
        if (currentStateIsSelection) {
            var mouseupX = d3.event.clientX-horizontalShift;
            //pass selection box menu width and height
			var pos = adjustMenuPosition($('#brushMenu.menu').width(), $('#brushMenu.menu').height());
            selectedGenomeEnd = xscale_copy.invert(mouseupX);
            
            mySymbolList = geneArr.concat(cancerGeneArr);  
            var genes = [];
            if (selectedGenomeStart > selectedGenomeEnd)
                genes = $.captureSymbols(selectedGenomeEnd, selectedGenomeStart, mySymbolList, selectedChrom); 
            else 
                genes = $.captureSymbols(selectedGenomeStart, selectedGenomeEnd, mySymbolList, selectedChrom);
            
			showGenes(genes, (selectedChrom.name).substring(3), Math.floor(selectedGenomeStart), Math.floor(selectedGenomeEnd), pos);
        }
        currentStateIsSelection = false;
    }
	function adjustMenuPosition(menuW, menuH){
			var mouseX = d3.event.clientX,
			    mouseY = d3.event.clientY;
			    			
			//changed when zoom/pan!!!
			var bbox = svg.node().getBBox(),
				plotLeft = bbox.x,
				plotTop = bbox.y,
				plotWidth = bbox.width,
				plotHeight = bbox.height;
			
			if (debug) {
				console.log ("box dimension: "+plotLeft+" "+plotTop+" "+plotWidth+" "+plotHeight);
			}
			
			var menuWidth = menuW;
			    menuHeight = menuH;
			
			var padding = 30;
		  	
			var hPos = mouseX + plotLeft + padding;
			var vPos = mouseY + plotTop + padding;
			if (debug) {
				console.log ("hpos = "+hPos+" vpos = "+vPos);
			}
			//It is too close to the left.It handles zoom/pan action as well
			if ( hPos < plotGeometry.sideChrWidth ) hPos = menuWidth + padding;
			//It is too close to the right, 
			if ( (hPos + menuWidth) > plotWidth ){
				if (debug) console.log("close to right ...")			
				hPos = plotWidth - menuWidth - padding;
			}
			
			//It is too close to the bottom
			if ( (vPos - headerHeight + menuHeight) > plotHeight ) {
				if (debug) console.log("close to bottom ..")
				vPos = vPos - menuHeight - 2*padding ;
			}
			
			return {x: hPos, y: vPos};		
	}
	
    function showGenes(genes, chrom, start, end,  pos){
        if (genes.length){
            deactivateZoom();		
            brushClick(genes, chrom, start, end, pos);                                       
        }  
        else {
            removeSelectionBox();
            hideMenu();
            reactivateZoom();
        }
    }
        
    function mouseDownOnAChromosome(svgElement, t) {                  
        //if it's a left mouse down, then do 
        if (d3.event.which === 1 )  {            
             
            //activate selection mode
            function activateSelection(){
                createSelectionBox();
                //dynamically filled the selection box attributes
                selectionBox .attr("x", mousedownX ).attr("y", selectedYpos - spaceBetweenChromosome/5 ).attr("height", spaceBetweenChromosome);
                deactivateZoom();
            }
            //if shiftkey is pressed
            if(d3.event.shiftKey){
            
                d3.event.preventDefault();  
                d3.event.stopPropagation(); 
				
                //####clear previous selection, this allows when one selection is done, menu up, start to make another new selection
                removeSelectionBox();
                hideMenu();
  
                mousedownX = d3.event.clientX-horizontalShift; 
                selectedGenomeStart = xscale_copy.invert(mousedownX);
                
                selectedChrom = t;
             
                svgrect = svgElement.getBBox();
                selectedYpos = svgrect.y;
                
                activateSelection();
                currentStateIsSelection = true;               
                  
                svg.on("mousemove", function(){ 
                    selectionmove(mousedownX, svgrect)
                });
                        
                if (d3.event.which ===1 )  {
                    //only for left mouseup;
                    //mouseup at any body position, use the mousedownx and mouseupX to track the genome region selected
                    d3.select("body").on("mouseup", function() {                    
                        mouseup(selectedGenomeStart, selectedChrom)
                    });  
                }
                /*d3.select("body").on("mouseout", function() {
                    removeSelectionBox();
                    hideMenu();                           
                    reactivateZoom();
                    currentStateIsSelection = false;
                })*/                 
            } //end of if shiftKey
        }//end of if(d3.event.which===1)
    }
    
    function isOncogene(symbolList){
        if (symbolList !== null ) {
            symbolList.forEach(function (x) {
                oncogeneDataCopy.forEach(function (d) {
                    if (x.geneSmashInfo.Symbol === d.geneSmashInfo.Symbol){
                        //console.log(x.geneSmashInfo.Symbol);
                        x.labeltype="oncogenelabelplus";
                        oncogeneDataCopy = removeAnElementFromCancerList(d, oncogeneDataCopy)  				
                    }
                });
            });
        }
    }
   
    function isSuppressor(symbolList){
        if (symbolList !== null ) {
            symbolList.forEach(function (x) {
                suppressorDataCopy.forEach(function (d) {
                    if (x.geneSmashInfo.Symbol === d.geneSmashInfo.Symbol){
                        x.labeltype ="suppressorlabelplus";
                        suppressorDataCopy = removeAnElementFromCancerList(d, suppressorDataCopy);
                    }
                });
            });
        }
    }
    function removeAnElementFromCancerList(element, list){
        list.forEach(function (d) {
            if (element.geneSmashInfo.Symbol === d. geneSmashInfo.Symbol ) { 		
                
                var index = list.indexOf(d);  			
                if (index > -1) {
                    list.splice(index ,1);
                }
            }
        });
        return list;
    }
    function removeAnElementFromSymbolList(element, list){
        
		var index;
        list.forEach(function (d) {
            if (element.geneSmashInfo.Symbol === d. geneSmashInfo.Symbol && 
                d.classtype === "gene2" ) {
                index = list.indexOf(d);  			
                if (index > -1) {
                    list.splice(index ,1);
                }
            }
			else if (element.geneSmashInfo.miRbase === d. geneSmashInfo.miRbase && 
				d.classtype === "mir2") {
                index = list.indexOf(d);  			
                if (index > -1) {
                    list.splice(index ,1);
                }
            }
        });
		
        return list;
    }
    //if a gene appears in both genelist1 and genelist2, remove the duplicated one with 
    //classtype = "gene2" from symbol list
    function isInterGene(symbolList){
       
       symbolList.forEach(function (x) {
            interGenelist.forEach(function (d) {
                if (x.geneSmashInfo.Symbol === d ){
                    symbolList = removeAnElementFromSymbolList(x, symbolList);   				
                }
            });
        });
        
    }
    //if a microRNAId appears in both mirlist1 and mirlist2, remove the duplicated one with 
    //classtype = "mir2" from symbol list
    function isInterMir(symbolList){
       symbolList.forEach(function (x) {
            interMirlist.forEach(function (d) {
                if (x.geneSmashInfo.miRbase === d ){
                    symbolList = removeAnElementFromSymbolList(x, symbolList);   				
                }
            });
        });
        
    }
    function updateCancergeneCopyData (symbolList){
        //console.log("updateCancergeneCopyData ...") 	
        isOncogene(symbolList) 
        isSuppressor(symbolList)   		
    }
    
    function updateParamList(symbolList){
        //console.log("updating paramlist")
        if (interGenelist !== null)
            isInterGene(symbolList);
        if (interMirlist !== null)
            isInterMir(symbolList);
    }
	 function processSymbolListForDisplay(inputSymbolList){
			var outputSymbolList;
		
			if (!inputSymbolList){
				return null;
			}
		
			//sort by chromosome/displayRowid   
			inputSymbolList.sort(function(a,b) {
				return a.displayRowid - b.displayRowid;
			}); 
		
			if (inputSymbolList.length === 1){
				outputSymbolList = inputSymbolList;
			}
			else {
				outputSymbolList = sortChromosomeByCodeStart(inputSymbolList);
			}
		
			outputSymbolList = markDisplayFlag(outputSymbolList);
			return outputSymbolList;
		}
	
		// ----------------------------------------------
		//sort mySymbolList1 by start code for each chromosome
        //put the result in mySymbolList
        function sortChromosomeByCodeStart (mySymbolList1){
		
           //for each chromosome, ordered by its TranscriptionStart
           
 		    var prevObj ;
            var tmp=[];
            var curObj;
            mySymbolList =[];
           
            for (var i =1; i< mySymbolList1.length; i++){
               
                if (i === 1) {
                    prevObj = mySymbolList1[0];
                    tmp.push(prevObj);
                }
                curObj = mySymbolList1[i];
               
                //if they are on the same chromosome
                if (prevObj.displayRowid === curObj.displayRowid) {  
                    tmp.push(curObj);
                    prevObj = curObj;
                    if (i === mySymbolList1.length -1 ){  //if it is the last element
                        sortChromosomeByCodeStartHelper(tmp, mySymbolList);
                    }                  
                }
                else {
                    if (i === mySymbolList1.length -1 ){  //if it is the last element
                        sortChromosomeByCodeStartHelper(tmp, mySymbolList);
                        mySymbolList.push(curObj);
                    }
                    else {                         
                        if (tmp.length === 1) {          //one gene on a chromosome                              
                            mySymbolList.push(prevObj);  //push that gene in mySymbolList, do not sort                      
                        }
                        else {
                            sortChromosomeByCodeStartHelper(tmp, mySymbolList);
                        }
                        //console.log("chromosome "+tmp[0].displayRowid+" has length " + tmp.length)                  
                        
                        tmp = [];
                        prevObj = curObj;
                        tmp.push(curObj);
                    
                    }//end of else
                }          
            }
            return mySymbolList;     
        }//end of sortChromosomeByCodeStart
		
        //algorithm: for each gene on the chromosome, if its neighbor symbols are too close to lie within
        //a threshold, mark it do not display, by adding display=0 to that gene object
		//extraInfo: to provide information for a symbol's nearby unlabelled symbols
        function markDisplayFlag (mytmp) {
            //console.log("markDisplayFlag() .....")
            
            var prevObj={};
            var curObj={};
			
            
            for (var i =1; i< mytmp.length; i++){
                if (i===1 ){
                    prevObj = mytmp[0];
					prevObj["extraInfo"] = undefined;
                }
                curObj = mytmp[i];
				//initialize extraInfo
                curObj["extraInfo"] = undefined; 
				
                if (prevObj.displayRowid === curObj.displayRowid) {
            	   
                    if (IsCloseBy(prevObj, curObj)){
                        prevObj["display"] = 0;
                        curObj["display"] = 1;      //show the second symbol if two symbols are too close      
						//record curObj with extra information: prevObj is not shown
						if (prevObj["extraInfo"] !== undefined)				
							curObj["extraInfo"] = prevObj.geneSmashInfo.Symbol + ","+prevObj.extraInfo;
						else 					
							curObj["extraInfo"] = prevObj.geneSmashInfo.Symbol;
                    }
                    else {
                        prevObj["display"] = 1;
                        curObj["display"] = 1;
                    }
                }
                //if prevObj is the last symbol on a chromosome, still show its label
                else {
                    prevObj["display"] = 1; 
                }  
                prevObj = curObj;          	           
            }
            return mytmp;
        }
		
		 //check if two gene objects a and b are close by their transcription start code
        function IsCloseBy(a,b) {
            var threshold = 35;
            //console.log("a = "+a.geneSmashInfo.Symbol+" b="+b.geneSmashInfo.Symbol)
            if (a.geneSmashInfo.Symbol === b.geneSmashInfo.Symbol){ 
                return false;        
            }   
            if (a.geneSmashInfo.miRbase !== undefined && b.geneSmashInfo.miRbase !== undefined){
                if (a.geneSmashInfo.miRbase === b.geneSmashInfo.miRbase )
                    return false;
            }
            var len1;
            var len2;
            var apos;
            var bpos;
           
            if (loadFromCancerGene(a)){            
                apos = xscale(a.geneSmashInfo.TranscriptionStart);
                //a and b are both loaded from cancer gene file
                if (loadFromCancerGene(b)){ 
               
                    bpos = xscale(b.geneSmashInfo.TranscriptionStart);            
                    if (Math.abs(apos-bpos)<=threshold){
                        return true;
                    }
                    else return false;            
                }
                //b from geneSmashService call
                else {
                    //b is from geneSmashService call
                    if (b.geneSmashInfo.Maps !== undefined ){
                        len2 = b.geneSmashInfo.Maps.length;
                        if (b.geneSmashInfo.Maps[len2-1] !== undefined ){
                            bpos = xscale(b.geneSmashInfo.Maps[len2-1].TranscriptionStart);
                            if (Math.abs(apos - bpos)<=threshold){
                                return true;
                            }                  
                            else  {                  
                                return false;
                            }
                        }
                    }
                }
                
            } // end of if
            
            //a is from geneSmashService call
            else {            
                if (loadFromCancerGene(b)){
                    bpos = xscale(b.geneSmashInfo.TranscriptionStart);
                    if (a.geneSmashInfo.Maps !== undefined ){
                        len1= a.geneSmashInfo.Maps.length;
                        if (a.geneSmashInfo.Maps[len1-1] !== undefined ){
                            apos = xscale(a.geneSmashInfo.Maps[len1-1].TranscriptionStart);
                            if (Math.abs( apos-bpos)<=threshold){
                                return true;
                            }
                            else return false;
                        }
                    }
                }
                // b is from geneSmash service call as well
                else {   
                    if (a.geneSmashInfo.Maps !== undefined && b.geneSmashInfo.Maps !== undefined ) { 
                        len1 = a.geneSmashInfo.Maps.length;
                        len2 = b.geneSmashInfo.Maps.length;
                        if (a.geneSmashInfo.Maps[len1-1] !== undefined && b.geneSmashInfo.Maps[len2-1] !== undefined  ){
                            apos = xscale(a.geneSmashInfo.Maps[len1-1].TranscriptionStart);
                            bpos = xscale(b.geneSmashInfo.Maps[len2-1].TranscriptionStart);
                                
                            if (Math.abs(apos-bpos)<=threshold){
                                return true;
                            }
                            else return false;
                        }
                    }             
                }
            }
            return false;           
        }
		
		  
        //sort genes in tmp array by their Transcription start code;
        //push elements in tmp to mySymbolList
        function sortChromosomeByCodeStartHelper(tmp, mySymbolList ){
            tmp.sort(function(a,b) {
                return sortHelper(a,b);
            })  
            tmp.forEach(function (d) {
                mySymbolList.push(d);
            })
        }
       
        
        //input a and b are gene objects from calling geneSmash web service or from oncogene/suppressor list
        //sorted by TranscriptionStart
        //precondition: object a and b is defined
        function sortHelper (a,b){     
            var len1;
            var len2;
            
            if (loadFromCancerGene(a)){
                //a and b are both cancer genes loaded from file
                if (loadFromCancerGene(b)){ 
                    return a.geneSmashInfo.TranscriptionStart - b.geneSmashInfo.TranscriptionStart;
                }
                //b from geneSmashService call
                else {
                    //b is from geneSmashService call
                    if (b.geneSmashInfo.Maps !== undefined ){
                        len2 = b.geneSmashInfo.Maps.length;
                        if (b.geneSmashInfo.Maps[len2-1] !== undefined ){
                            return a.geneSmashInfo.TranscriptionStart - b.geneSmashInfo.Maps[len2-1].TranscriptionStart;
                        }
                    }
                    else {
                        console.log ("sortHelper(): "+b.geneSmashInfo.Symbol+" does not have geneSmash Map info")
                    }
                }
                
            } // end of if a is loaded from cancergene 
            
            //a is from geneSmashService call
            else {
                if (loadFromCancerGene(b)){
                    if (a.geneSmashInfo.Maps !== undefined ){
                        len1= a.geneSmashInfo.Maps.length;
                        if (a.geneSmashInfo.Maps[len1-1] !== undefined ){
                            return a.geneSmashInfo.Maps[len1-1].TranscriptionStart - b.geneSmashInfo.TranscriptionStart;
                        }
                    }
                }
                // b is from geneSmash service call as well
                else {
                    if (a.geneSmashInfo.Maps !== undefined && b.geneSmashInfo.Maps !== undefined ) { 
                        len1 = a.geneSmashInfo.Maps.length;
                        len2 = b.geneSmashInfo.Maps.length;
                        if (a.geneSmashInfo.Maps[len1-1] !== undefined && b.geneSmashInfo.Maps[len2-1] !== undefined  )
                            return a.geneSmashInfo.Maps[len1-1].TranscriptionStart- b.geneSmashInfo.Maps[len2-1].TranscriptionStart;
                    }
                    else {
                        console.log ("sortHelper(): "+a.geneSmashInfo.Symbol+" and/or "+b.geneSmashInfo.Symbol+" do not have geneSmash Map info ");
                    }
                }
            }
        }
	
    // Return module interface.
    return {        
        createIdeogram: createIdeogram,
        //the following functions can be also invoked by Ideogram object.
        zoomIn: zoomIn,
        zoomOut: zoomOut,
        resetScale: resetScale,
        reactivateZoom: reactivateZoom,
        removeSelectionBox: removeSelectionBox,
        removeOncogene: removeOncogene,
        removeSuppressor: removeSuppressor,
        redraw: redraw,
        resizePlot: resizePlot
    };

})();  //end of Ideogram

