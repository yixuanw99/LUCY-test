(function(){"use strict";var e={104:function(e,t,a){var i=a(751),s=a(641);const o={id:"app"};function r(e,t,a,i,r,n){const c=(0,s.g2)("router-view");return(0,s.uX)(),(0,s.CE)("div",o,[(0,s.bF)(c)])}var n={name:"App"},c=a(262);const l=(0,c.A)(n,[["render",r]]);var d=l,u=a(220);const h={class:"fetch-report"},p={class:"input-section"};function k(e,t,a,o,r,n){return(0,s.uX)(),(0,s.CE)("div",h,[t[2]||(t[2]=(0,s.Lk)("h1",null,"獲取樂稀表觀檢測報告",-1)),(0,s.Lk)("div",p,[(0,s.bo)((0,s.Lk)("input",{"onUpdate:modelValue":t[0]||(t[0]=e=>o.inputSampleId=e),placeholder:"輸入樣本ID"},null,512),[[i.Jo,o.inputSampleId]]),(0,s.Lk)("button",{onClick:t[1]||(t[1]=(...e)=>o.fetchReport&&o.fetchReport(...e))},"獲取報告")])])}var g=a(953),f={name:"FetchReport",setup(){const e=(0,g.KR)(""),t=(0,u.rd)(),a=async()=>{try{const a=await fetch("/LUCY-test/mockdata/mock-data.json"),i=await a.json(),s=i.reports.findIndex((t=>t.sample_id===e.value));-1!==s?(localStorage.setItem("reportData",JSON.stringify(i.reports[s])),t.push({name:"ReportDisplay",params:{id:e.value}})):alert("無法找到匹配的報告，請檢查樣本ID是否正確。")}catch(a){console.error("Error fetching mock report:",a),alert("無法獲取報告，請稍後再試。")}};return{inputSampleId:e,fetchReport:a}}};const v=(0,c.A)(f,[["render",k],["__scopeId","data-v-ab6298ee"]]);var m=v,b=a(33),x=a.p+"img/logo.773f83ce.png",L=a.p+"img/share_button.890f936d.png";const y={class:"lucy-report"},R={style:{paddingTop:"90px"}},w={class:"user-info"},C={class:"info-grid"},P={class:"info-item"},E={class:"info-value"},A={class:"info-item"},$={class:"info-value"},_={class:"info-item"},F={class:"info-value"},D={class:"info-item"},I={class:"info-value"},N={key:0},S={id:"biological-age",class:"section"},W={class:"section-title"},z={class:"section-content"},B={class:"section-text"},V=["innerHTML"],U={class:"section-figure"},M={id:"aging-speed",class:"section"},O={class:"section-title"},K=["href"],j={class:"section-content"},X={class:"section-text"},T=["innerHTML"],H={class:"section-figure"},q={id:"disease-risks",class:"section"},Y={class:"section-title"},G=["href"],J={class:"section-content"},Q={class:"section-figure"},Z={class:"table-and-description"};function ee(e,t,a,o,r,n){const c=(0,s.g2)("GaugeChart"),l=(0,s.g2)("AgingSpeedPlot"),d=(0,s.g2)("disease-risks-table"),u=(0,s.g2)("disease-risks-plot");return(0,s.uX)(),(0,s.CE)("div",y,[t[19]||(t[19]=(0,s.Fv)('<header data-v-14771c4b><div class="header-title" data-v-14771c4b><h1 data-v-14771c4b>樂稀表觀檢測報告</h1><nav class="report-nav" data-v-14771c4b><a href="#biological-age" data-v-14771c4b>生物年齡</a><a href="#aging-speed" data-v-14771c4b>老化速度</a><a href="#disease-risks" data-v-14771c4b>老化疾病風險評估</a></nav><div class="logo-container" data-v-14771c4b><img class="logo" src="'+x+'" alt="LUCY logo" data-v-14771c4b><b class="logo-text" data-v-14771c4b>LUCY</b></div></div></header>',1)),(0,s.Lk)("main",R,[(0,s.Lk)("div",w,[t[5]||(t[5]=(0,s.Lk)("h2",null,"Information",-1)),(0,s.Lk)("div",C,[(0,s.Lk)("div",P,[t[1]||(t[1]=(0,s.Lk)("span",{class:"info-label"},"姓名：",-1)),(0,s.Lk)("span",E,(0,b.v_)(o.info.name),1)]),(0,s.Lk)("div",A,[t[2]||(t[2]=(0,s.Lk)("span",{class:"info-label"},"樣本編號：",-1)),(0,s.Lk)("span",$,(0,b.v_)(o.info.sampleId),1)]),(0,s.Lk)("div",_,[t[3]||(t[3]=(0,s.Lk)("span",{class:"info-label"},"採檢日期：",-1)),(0,s.Lk)("span",F,(0,b.v_)(o.info.collectionDate),1)]),(0,s.Lk)("div",D,[t[4]||(t[4]=(0,s.Lk)("span",{class:"info-label"},"報告日期：",-1)),(0,s.Lk)("span",I,(0,b.v_)(o.info.reportDate),1)])])]),o.reportData?((0,s.uX)(),(0,s.CE)("div",N,[(0,s.Lk)("section",S,[(0,s.Lk)("div",W,[t[7]||(t[7]=(0,s.Lk)("h2",null,"生物年齡",-1)),(0,s.Lk)("a",{class:"cta",onClick:t[0]||(t[0]=(0,i.D$)((()=>o.shareSection("biological-age")),["prevent"]))},t[6]||(t[6]=[(0,s.Lk)("img",{alt:"share_button",src:L,width:"20"},null,-1)]))]),t[9]||(t[9]=(0,s.Lk)("hr",{width:"100%",size:"3",color:"#80c2ec",style:{"margin-top":"0px"}},null,-1)),(0,s.Lk)("div",z,[(0,s.Lk)("div",B,[t[8]||(t[8]=(0,s.Lk)("p",null,"表觀遺傳時鐘（Epigenetic Clock）是一種根據DNA甲基化水平來預測生物年齡的工具。DNA甲基化是影響基因表達的化學修飾，隨著年齡增長會發生變化。表觀遺傳時鐘通過測量特定DNA位點的甲基化程度來估算個體的生物年齡，這種方法可用於評估健康狀況、老化速度，甚至預測疾病風險。",-1)),(0,s.Lk)("p",{innerHTML:o.bioAgeComment},null,8,V)]),(0,s.Lk)("div",U,[(0,s.bF)(c,{"bio-age":o.formattedBioAge,"chro-age":o.formattedChroAge,width:450},null,8,["bio-age","chro-age"])])])]),(0,s.Lk)("section",M,[(0,s.Lk)("div",O,[t[11]||(t[11]=(0,s.Lk)("h2",null,"老化速度",-1)),(0,s.Lk)("a",{class:"cta",href:"https://www.facebook.com/sharer.php?u="+o.agingSpeedFigUrl},t[10]||(t[10]=[(0,s.Lk)("img",{alt:"share_button",src:L,width:"20"},null,-1)]),8,K)]),t[14]||(t[14]=(0,s.Lk)("hr",{width:"100%",size:"3",color:"#80c2ec",style:{"margin-top":"0px"}},null,-1)),(0,s.Lk)("div",j,[(0,s.Lk)("div",X,[t[12]||(t[12]=(0,s.Lk)("p",null,"老化速度是一種測量個體老化速度的指標，基於紐西蘭Dunedin縱向研究的數據發展而來。它利用DNA甲基化的變化來評估身體系統的衰老速率。老化速度能夠顯示”當下”跟同齡人相比老的快還是慢。這個指標幫助研究者和受測者了解老化進程，提供個性化的健康干預建議。",-1)),t[13]||(t[13]=(0,s.Lk)("p",null,"老化速度反映的是老化當前動態變化，類似於加速器。即使 一個人Horvath 顯示生物年齡比實際年齡輕，也可能 DunedinPACE 顯示老化速率加快。",-1)),(0,s.Lk)("p",{innerHTML:o.paceComment},null,8,T)]),(0,s.Lk)("div",H,[(0,s.bF)(l,{"pace-value":o.formattedPaceValue,"pace-pr":o.pacePrInverse,width:450},null,8,["pace-value","pace-pr"])])])]),(0,s.Lk)("section",q,[(0,s.Lk)("div",Y,[t[16]||(t[16]=(0,s.Lk)("h2",null,"老化疾病風險評估",-1)),(0,s.Lk)("a",{class:"cta",href:"https://www.facebook.com/sharer.php?u="+o.diseaseRisksFigUrl},t[15]||(t[15]=[(0,s.Lk)("img",{alt:"share_button",src:L,width:"20"},null,-1)]),8,G)]),t[18]||(t[18]=(0,s.Lk)("hr",{width:"100%",size:"3",color:"#80c2ec",style:{"margin-top":"0px"}},null,-1)),(0,s.Lk)("div",J,[(0,s.Lk)("div",Q,[(0,s.Lk)("div",Z,[(0,s.bF)(d,{"disease-risks":o.diseaseRisks},null,8,["disease-risks"]),t[17]||(t[17]=(0,s.Lk)("p",null,"placeholder還不確定這邊的文案放甚麼",-1))]),(0,s.bF)(u,{"disease-risks":o.diseaseRisks},null,8,["disease-risks"])])])])])):(0,s.Q3)("",!0)]),(0,s.Lk)("footer",null,[(0,s.Lk)("p",null,"© "+(0,b.v_)((new Date).getFullYear())+" LUCY. All rights reserved.",1)])])}var te=a(354),ae=a.n(te);const ie=["width","height","viewBox"],se=["x"],oe=["x"],re={"font-weight":"bold"},ne=["x","y","font-size"],ce=["x","y","font-size"],le=["x1","y1","x2","y2","stroke-width"],de=["transform"],ue=["d","transform"],he=["y","width","height"],pe=["cx","cy","r"],ke=["x","y","font-size"],ge=["y","font-size"],fe=["transform"],ve=["d","transform"],me=["y","width","height"],be=["cx","cy","r"],xe=["x","y","font-size"],Le=["y","font-size"];function ye(e,t,a,i,o,r){return(0,s.uX)(),(0,s.CE)("svg",{width:a.width,height:i.height,viewBox:`0 0 ${a.width} ${i.height}`},[(0,s.Lk)("text",{x:a.width/2,y:"40","text-anchor":"middle","font-size":"14","font-family":"Lucida Console"},"Based on the methylation pattern of your saliva,",8,se),(0,s.Lk)("text",{x:a.width/2,y:"60","text-anchor":"middle","font-size":"14","font-family":"Lucida Console"},[t[0]||(t[0]=(0,s.eW)("your Biological Age is ")),(0,s.Lk)("tspan",re,(0,b.v_)(a.bioAge),1),t[1]||(t[1]=(0,s.eW)("."))],8,oe),(0,s.Lk)("text",{x:.1*a.width,y:.667*i.height,"text-anchor":"middle","font-size":.024*a.width,"font-family":"Lucida Console"},"0",8,ne),(0,s.Lk)("text",{x:.9*a.width,y:.667*i.height,"text-anchor":"middle","font-size":.024*a.width,"font-family":"Lucida Console"},"100",8,ce),(0,s.Lk)("line",{x1:.1*a.width,y1:.6*i.height,x2:.9*a.width,y2:.6*i.height,stroke:"#E0E0E0","stroke-width":.008*a.width},null,8,le),(0,s.Lk)("g",{transform:`translate(${i.bioAgePosition}, ${.733*i.height})`},[(0,s.Lk)("path",{d:i.bioAgePin,transform:`translate(${.052*-a.width}, ${.433*-i.height}) scale(1)`,fill:"#4CAF50"},null,8,ue),(0,s.Lk)("rect",{x:0,y:.147*-i.height,width:.008*a.width,height:.027*i.height,fill:"#4CAF50"},null,8,he),(0,s.Lk)("circle",{cx:.008*a.width,cy:.333*-i.height,r:.044*a.width,fill:"#4CAF50"},null,8,pe),(0,s.Lk)("text",{x:.008*a.width,y:.335*-i.height,"text-anchor":"middle",fill:"white","font-size":.034*a.width,"font-weight":"bold","font-family":"Lucida Console"},(0,b.v_)(a.bioAge),9,ke),(0,s.Lk)("text",{x:0,y:.467*-i.height,"text-anchor":"middle","font-size":.024*a.width,"font-family":"Lucida Console","font-weight":"bold"},"Biological Age",8,ge)],8,de),(0,s.Lk)("g",{transform:`translate(${i.chroAgePosition}, ${.733*i.height})`},[(0,s.Lk)("path",{d:i.chroAgePin,transform:`translate(${.03*-a.width}, ${.067*i.height}) scale(1, -1)`,fill:"#9E9E9E"},null,8,ve),(0,s.Lk)("rect",{x:0,y:.147*-i.height,width:.008*a.width,height:.027*i.height,fill:"#9E9E9E"},null,8,me),(0,s.Lk)("circle",{cx:.006*a.width,cy:.003*i.height,r:.024*a.width,fill:"#9E9E9E"},null,8,be),(0,s.Lk)("text",{x:.006*a.width,y:.02*i.height,"text-anchor":"middle",fill:"white","font-size":.032*a.width,"font-family":"Lucida Console"},(0,b.v_)(a.chroAge),9,xe),(0,s.Lk)("text",{x:0,y:.117*i.height,"text-anchor":"middle","font-size":.024*a.width,"font-family":"Lucida Console","font-weight":"bold"},"Calendar Age",8,Le)],8,fe)],8,ie)}var Re={name:"GaugeChart",props:{bioAge:{type:Number,required:!0},chroAge:{type:Number,required:!0},width:{type:Number,default:500}},setup(e){const t=(0,s.EW)((()=>.75*e.width)),a=(0,s.EW)((()=>t=>.1*e.width+t/100*(.8*e.width))),i=(0,s.EW)((()=>a.value(e.bioAge))),o=(0,s.EW)((()=>a.value(e.chroAge))),r=e=>`\n      M${30*e},0 \n      C${13.4*e},0 0,${13.4*e} 0,${30*e} \n      C0,${51.6*e} ${30*e},${75*e} ${30*e},${75*e} \n      C${30*e},${75*e} ${60*e},${51.6*e} ${60*e},${30*e} \n      C${60*e},${13.4*e} ${46.6*e},0 ${30*e},0 \n      Z\n    `,n=(0,s.EW)((()=>r(e.width/500))),c=(0,s.EW)((()=>r(e.width/500*.6)));return{height:t,bioAgePosition:i,chroAgePosition:o,bioAgePin:n,chroAgePin:c}}};const we=(0,c.A)(Re,[["render",ye]]);var Ce=we;const Pe=["width","height"],Ee=["d"],Ae=["x"],$e=["x1","x2"],_e=["cx"],Fe=["cx"],De=["cx"],Ie=["x1","x2"],Ne=["x"],Se=["x"];function We(e,t,a,i,o,r){return(0,s.uX)(),(0,s.CE)("svg",{width:a.width,height:i.height,viewBox:"0 0 400 300"},[t[0]||(t[0]=(0,s.Lk)("rect",{x:"0",y:"0",width:"400",height:"300",fill:"#ffffff"},null,-1)),t[1]||(t[1]=(0,s.Lk)("line",{x1:"50",y1:"250",x2:"350",y2:"250",stroke:"black"},null,-1)),(0,s.Lk)("path",{d:i.normalDistributionPath,fill:"#a2def4",stroke:"none"},null,8,Ee),((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(i.xAxisTicks,(e=>((0,s.uX)(),(0,s.CE)("g",{key:e},[(0,s.Lk)("text",{x:i.xScale(e),y:"275","text-anchor":"middle"},(0,b.v_)(e),9,Ae)])))),128)),(0,s.Lk)("line",{x1:i.xScale(a.paceValue),y1:"90",x2:i.xScale(a.paceValue),y2:"250",stroke:"black","stroke-dasharray":"5,5"},null,8,$e),(0,s.Lk)("circle",{cx:i.xScale(a.paceValue),cy:"90",r:"3",fill:"black"},null,8,_e),(0,s.Lk)("circle",{cx:i.xScale(a.paceValue),cy:"250",r:"3",fill:"black"},null,8,Fe),(0,s.Lk)("circle",{cx:i.xScale(a.paceValue)+165,cy:"140",r:"3",fill:"black"},null,8,De),(0,s.Lk)("line",{x1:i.xScale(a.paceValue),y1:"140",x2:i.xScale(a.paceValue)+165,y2:"140",stroke:"black","stroke-dasharray":"5,5"},null,8,Ie),(0,s.Lk)("text",{x:i.xScale(a.paceValue),y:"70","text-anchor":"middle","font-weight":"bold"},(0,b.v_)(a.paceValue),9,Ne),(0,s.Lk)("text",{x:i.xScale(a.paceValue)+5,y:"130","font-size":"14",fill:"black"},"你比"+(0,b.v_)(a.pacePr)+"%同齡的人老得慢",9,Se),t[2]||(t[2]=(0,s.Lk)("text",{x:"200",y:"295","text-anchor":"middle"},"你的老化速度",-1))],8,Pe)}var ze={name:"AgingSpeedPlot",props:{paceValue:{type:Number,required:!0},pacePr:{type:Number,required:!0},width:{type:Number,default:400}},setup(e){const t=(0,s.EW)((()=>.75*e.width)),a=(e,t=1,a=.2)=>Math.exp(-.5*Math.pow((e-t)/a,2))/(a*Math.sqrt(2*Math.PI)),i=(0,s.EW)((()=>e=>50+e/2*300)),o=(0,s.EW)((()=>{const e=[];for(let t=.4;t<=1.6;t+=.005){const s=a(t);e.push([i.value(t),250-50*s])}return"M"+e.map((e=>e.join(","))).join("L")})),r=(0,g.KR)([0,.2,.4,.6,.8,1,1.2,1.4,1.6,1.8,2]);return{height:t,normalDistributionPath:o,xScale:i,xAxisTicks:r}}};const Be=(0,c.A)(ze,[["render",We]]);var Ve=Be;const Ue={class:"overflow-x-auto"},Me={class:"min-w-full bg-white border border-gray-300"},Oe={class:"py-2 px-4 border-b row-name"},Ke={class:"py-2 px-4 border-b content"},je={class:"py-2 px-4 border-b content"};function Xe(e,t,a,i,o,r){return(0,s.uX)(),(0,s.CE)("div",Ue,[(0,s.Lk)("table",Me,[t[0]||(t[0]=(0,s.Lk)("thead",null,[(0,s.Lk)("tr",{class:"bg-gray-100"},[(0,s.Lk)("th",{class:"py-2 px-4 border-b"},"疾病風險"),(0,s.Lk)("th",{class:"py-2 px-4 border-b column-name"},"當前DunedinPACE風險"),(0,s.Lk)("th",{class:"py-2 px-4 border-b column-name"},"若DunedinPACE減少0.05時風險")])],-1)),(0,s.Lk)("tbody",null,[((0,s.uX)(!0),(0,s.CE)(s.FK,null,(0,s.pI)(i.risks,(e=>((0,s.uX)(),(0,s.CE)("tr",{key:e.name,class:"hover:bg-gray-50"},[(0,s.Lk)("td",Oe,(0,b.v_)(e.name),1),(0,s.Lk)("td",Ke,(0,b.v_)(e.current)+" %",1),(0,s.Lk)("td",je,(0,b.v_)(e.reduced01)+" %",1)])))),128))])])])}var Te={name:"DiseaseRisksTable",props:{diseaseRisks:{type:Array,required:!0}},setup(e){const t=(0,s.EW)((()=>[{name:"全因死亡率",current:e.diseaseRisks[0].acmPaceRisk,reduced01:e.diseaseRisks[1].acmPaceRiskReduced01},{name:"心血管疾病",current:e.diseaseRisks[0].cvdPaceRisk,reduced01:e.diseaseRisks[1].cvdPaceRiskReduced01},{name:"糖尿病風險",current:e.diseaseRisks[0].dmPaceRisk,reduced01:e.diseaseRisks[1].dmPaceRiskReduced01},{name:"失智風險",current:e.diseaseRisks[0].adPaceRisk,reduced01:e.diseaseRisks[1].adPaceRiskReduced01},{name:"癌症風險",current:e.diseaseRisks[0].cancerPaceRisk,reduced01:e.diseaseRisks[1].cancerPaceRiskReduced01}]));return{risks:t}}};const He=(0,c.A)(Te,[["render",Xe],["__scopeId","data-v-d438590a"]]);var qe=He;const Ye={class:"chart-container"};function Ge(e,t,a,i,o,r){const n=(0,s.g2)("Radar");return(0,s.uX)(),(0,s.CE)("div",Ye,[(0,s.bF)(n,{data:e.chartData,options:e.chartOptions},null,8,["data","options"])])}var Je=a(527),Qe=a(22);Qe.t1.register(Qe.pr,Qe.FN,Qe.No,Qe.dN,Qe.m_,Qe.s$);var Ze=(0,s.pM)({name:"DiseaseRisksPlot",components:{Radar:Je.Vd},props:{diseaseRisks:{type:Array,required:!0}},setup(e){const t=(0,s.EW)((()=>({labels:["全因死亡率","心血管疾病","糖尿病風險","失智風險","癌症風險"],datasets:[{label:"當前DunedinPACE風險(%)",backgroundColor:"rgba(54, 162, 235, 0.05)",borderColor:"rgba(54, 162, 235, 1)",pointBackgroundColor:"rgba(54, 162, 235, 1)",pointBorderColor:"#fff",pointHoverBackgroundColor:"#fff",pointHoverBorderColor:"rgba(75, 192, 192, 1)",data:[e.diseaseRisks[0].acmPaceRisk,e.diseaseRisks[0].cvdPaceRisk,e.diseaseRisks[0].dmPaceRisk,e.diseaseRisks[0].adPaceRisk,e.diseaseRisks[0].cancerPaceRisk]},{label:"若DunedinPACE減少0.05時風險(%)",backgroundColor:"rgba(75, 192, 192, 0.2)",borderColor:"rgba(75, 192, 192, 1)",pointBackgroundColor:"rgba(75, 192, 192, 1)",pointBorderColor:"#fff",pointHoverBackgroundColor:"#fff",pointHoverBorderColor:"rgba(54, 162, 235, 1)",data:[e.diseaseRisks[1].acmPaceRiskReduced01,e.diseaseRisks[1].cvdPaceRiskReduced01,e.diseaseRisks[1].dmPaceRiskReduced01,e.diseaseRisks[1].adPaceRiskReduced01,e.diseaseRisks[1].cancerPaceRiskReduced01]}]}))),a={responsive:!0,maintainAspectRatio:!1,scales:{r:{angleLines:{display:!1},grid:{color:e=>0===e.tick.value?"rgba(0, 0, 0, 0.5)":"rgba(0, 0, 0, 0.1)",lineWidth:e=>0===e.tick.value?2:1},ticks:{backdropColor:"transparent",color:"rgba(0, 0, 0, 0.7)"}}}};return{chartData:t,chartOptions:a}}});const et=(0,c.A)(Ze,[["render",Ge],["__scopeId","data-v-a0405d68"]]);var tt=et,at={name:"EpigeneticReport",components:{GaugeChart:Ce,AgingSpeedPlot:Ve,DiseaseRisksTable:qe,DiseaseRisksPlot:tt},setup(){const e=(0,g.KR)(null),t=(0,g.Kh)({name:"",sampleId:"",collectionDate:"",reportDate:""}),a=(0,g.KR)(0),i=(0,g.KR)(0),o=(0,g.KR)(0),r=(0,g.KR)(0),n=(0,s.EW)((()=>parseFloat(a.value.toFixed(2)))),c=(0,s.EW)((()=>parseFloat(i.value.toFixed(1)))),l=(0,s.EW)((()=>parseFloat(o.value.toFixed(2)))),d=(0,s.EW)((()=>o.value-1)),h=(0,s.EW)((()=>[{acmPaceRisk:Number((200*d.value).toFixed(2)),cvdPaceRisk:Number((195*d.value).toFixed(2)),dmPaceRisk:Number((155*d.value).toFixed(2)),adPaceRisk:Number((200*d.value).toFixed(2)),cancerPaceRisk:Number((250*d.value).toFixed(2))},{acmPaceRiskReduced01:Number((200*(d.value-.05)).toFixed(2)),cvdPaceRiskReduced01:Number((195*(d.value-.05)).toFixed(2)),dmPaceRiskReduced01:Number((155*(d.value-.05)).toFixed(2)),adPaceRiskReduced01:Number((200*(d.value-.05)).toFixed(2)),cancerPaceRiskReduced01:Number((250*(d.value-.05)).toFixed(2))}])),p=(0,g.KR)(""),k=(0,g.KR)(""),f=(0,g.KR)(""),v=(0,s.EW)((()=>Math.abs(Math.round(100*(a.value-i.value))/100))),m=(0,s.EW)((()=>{const e=a.value-i.value,t=`根據你的表觀遺傳訊息，你的生物年齡為<strong>${n.value}</strong>歲`;if(Math.abs(e)<2)return`${t}。你的身體狀況與同齡人相比處於平均水平，這是一個良好的跡象。為了進一步優化健康狀況，你可以專注於一些小的改變，例如增加高強度的運動訓練，或者更加規律地進行壓力管理，這將有助於進一步提升你的健康指數。`;{const a=`，比你的實際年齡${c.value}歲要${e<0?"年輕":"老"}了<strong>${v.value}</strong>歲。`;return e<0?`${t}${a}恭喜你！代表跟同年齡的相比，統計上你有更長的餘命。這意味著你擁有健康的生活方式，讓你的生理機能維持在更年輕的水平。繼續保持這種積極的健康習慣，這將有助於進一步延緩老化速度，增強身體韌性和抵抗疾病的能力。保持這種正向的生活方式，例如規律運動、健康飲食、良好的睡眠和壓力管理，將能進一步鞏固你的健康優勢，延長壽命。`:`${t}${a}這可能表明你的身體正在承受更多的壓力或生活方式需要進行一定的調整，這將影響到你的整體健康。不要擔心，這是一個改善健康的好機會！你可以從一些關鍵生活領域開始進行調整，例如減少壓力、增加有氧運動、改善飲食結構，以及更加規律的睡眠習慣。這些變化將有助於降低你的生物年齡，讓你在未來的健康評估中獲得更積極的結果。`}})),b=(0,s.EW)((()=>{const e=l.value;let t=`你的老化速度為<strong>${e}</strong>，比<strong>${x.value}%</strong>同齡的人老得慢。代表平均一個人老1.0年，你的身體老了<strong>${e}</strong>年。數值越低，代表老化速度越慢。<br><br>`;return e>=.97&&e<=1.03?t+="你的老化速度處於<strong>正常範圍</strong>。這意味著你的老化速度與年齡增長的速度基本一致。":e>1.03&&e<1.2?t+="你的老化速度<strong>略快於正常</strong>。這表示你的衰老速度稍微加快，可能需要關注一些生活方式的調整。":e>=1.2?t+="你的老化速度<strong>明顯加快</strong>。這表示衰老速度加快，生理功能退化的風險增加。建議你積極採取措施改善生活方式，以減緩老化速度。":e<.97&&e>.8?t+="你的老化速度<strong>略慢於正常</strong>。這是一個好現象，表明你的生活方式可能對健康有積極影響。":e<=.8&&(t+="你的老化速度<strong>明顯減緩</strong>。這表明你的衰老速度比正常人慢，潛在的健康風險降低。繼續保持良好的生活習慣，有助於維持這種優勢。"),t})),x=(0,s.EW)((()=>100-r.value)),L=async e=>{try{const t=document.getElementById(`${e}`);if(!t)return void console.error(`Element with id ${e}-section not found`);const a=await ae()(t),i=a.toDataURL("image/png"),s=()=>window.location.href,o=encodeURIComponent(s()),r=`https://www.facebook.com/sharer.php?u=${o}&picture=${encodeURIComponent(i)}`;window.open(r,"_blank")}catch(t){console.error("Error generating or sharing image:",t)}},y=(0,u.lq)(),R=parseInt(y.params.id||"0",10);(0,s.sV)((async()=>{{const t=await fetch("/LUCY-test/mockdata/mock-data.json"),a=await t.json();e.value=a.reports[R]}w()}));const w=()=>{e.value&&(t.name=e.value.user_id,t.sampleId=e.value.sample_id,t.collectionDate=e.value.collection_date,t.reportDate=e.value.report_date,a.value=e.value.bio_age,i.value=e.value.chro_age,o.value=e.value.pace_value,r.value=e.value.pace_pr)};return{reportData:e,info:t,bioAge:a,chroAge:i,paceValue:o,formattedBioAge:n,formattedChroAge:c,formattedPaceValue:l,pacePr:r,diseaseRisks:h,epigeneticClockFigUrl:p,agingSpeedFigUrl:k,diseaseRisksFigUrl:f,diffAge:v,bioAgeComment:m,pacePrInverse:x,paceComment:b,shareSection:L}}};const it=(0,c.A)(at,[["render",ee],["__scopeId","data-v-14771c4b"]]);var st=it;const ot=[{path:"/",name:"FetchReport",component:m},{path:"/report/:id",name:"ReportDisplay",component:st,props:!0}],rt=(0,u.aE)({history:(0,u.LA)("/LUCY-test/"),routes:ot});var nt=rt;const ct=(0,i.Ef)(d);ct.use(nt),ct.mount("#app")}},t={};function a(i){var s=t[i];if(void 0!==s)return s.exports;var o=t[i]={exports:{}};return e[i].call(o.exports,o,o.exports,a),o.exports}a.m=e,function(){var e=[];a.O=function(t,i,s,o){if(!i){var r=1/0;for(d=0;d<e.length;d++){i=e[d][0],s=e[d][1],o=e[d][2];for(var n=!0,c=0;c<i.length;c++)(!1&o||r>=o)&&Object.keys(a.O).every((function(e){return a.O[e](i[c])}))?i.splice(c--,1):(n=!1,o<r&&(r=o));if(n){e.splice(d--,1);var l=s();void 0!==l&&(t=l)}}return t}o=o||0;for(var d=e.length;d>0&&e[d-1][2]>o;d--)e[d]=e[d-1];e[d]=[i,s,o]}}(),function(){a.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return a.d(t,{a:t}),t}}(),function(){a.d=function(e,t){for(var i in t)a.o(t,i)&&!a.o(e,i)&&Object.defineProperty(e,i,{enumerable:!0,get:t[i]})}}(),function(){a.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){a.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){a.p="/LUCY-test/"}(),function(){var e={524:0};a.O.j=function(t){return 0===e[t]};var t=function(t,i){var s,o,r=i[0],n=i[1],c=i[2],l=0;if(r.some((function(t){return 0!==e[t]}))){for(s in n)a.o(n,s)&&(a.m[s]=n[s]);if(c)var d=c(a)}for(t&&t(i);l<r.length;l++)o=r[l],a.o(e,o)&&e[o]&&e[o][0](),e[o]=0;return a.O(d)},i=self["webpackChunkepigenetic_report_vue3"]=self["webpackChunkepigenetic_report_vue3"]||[];i.forEach(t.bind(null,0)),i.push=t.bind(null,i.push.bind(i))}();var i=a.O(void 0,[504],(function(){return a(104)}));i=a.O(i)})();
//# sourceMappingURL=app.1adc9e7b.js.map