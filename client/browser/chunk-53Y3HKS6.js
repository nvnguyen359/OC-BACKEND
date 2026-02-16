import{a as Ce,b as ye}from"./chunk-W7NCV7QP.js";import{a as xe,b as ke}from"./chunk-FAAPNWCL.js";import"./chunk-GFRJEQFL.js";import{a as Te,b as De}from"./chunk-6Z233KJD.js";import"./chunk-BWPD25ZQ.js";import{d as Se}from"./chunk-GUACCTIK.js";import{$d as g,Ae as _e,Bb as c,Be as we,Cb as $,Fb as j,Gb as Q,Hb as v,Ib as E,Jc as Z,La as d,Lc as y,Nb as K,O as M,Ob as U,Od as A,P as V,Pb as b,Q as B,Qb as a,Re as ve,S as N,Sb as W,Sd as ee,Se as Ee,Td as S,U as h,Wd as te,Ya as w,Yb as C,Z as k,Za as I,Zd as ie,_ as T,_b as J,_d as ne,ab as O,bb as L,be as oe,cb as G,ce as re,ea as P,ee as le,fe as ae,ge as se,he as de,ib as f,lb as H,le as ue,ma as D,mb as q,me as ce,nc as X,ne as pe,pb as u,pe as ge,qb as i,qe as he,rb as n,sb as m,sc as F,se as _,tc as Y,te as me,ue as fe,ve as be,yb as R,zb as z}from"./chunk-T55JMWX5.js";var Fe=`
    .p-toggleswitch {
        display: inline-block;
        width: dt('toggleswitch.width');
        height: dt('toggleswitch.height');
    }

    .p-toggleswitch-input {
        cursor: pointer;
        appearance: none;
        position: absolute;
        top: 0;
        inset-inline-start: 0;
        width: 100%;
        height: 100%;
        padding: 0;
        margin: 0;
        opacity: 0;
        z-index: 1;
        outline: 0 none;
        border-radius: dt('toggleswitch.border.radius');
    }

    .p-toggleswitch-slider {
        cursor: pointer;
        width: 100%;
        height: 100%;
        border-width: dt('toggleswitch.border.width');
        border-style: solid;
        border-color: dt('toggleswitch.border.color');
        background: dt('toggleswitch.background');
        transition:
            background dt('toggleswitch.transition.duration'),
            color dt('toggleswitch.transition.duration'),
            border-color dt('toggleswitch.transition.duration'),
            outline-color dt('toggleswitch.transition.duration'),
            box-shadow dt('toggleswitch.transition.duration');
        border-radius: dt('toggleswitch.border.radius');
        outline-color: transparent;
        box-shadow: dt('toggleswitch.shadow');
    }

    .p-toggleswitch-handle {
        position: absolute;
        top: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        background: dt('toggleswitch.handle.background');
        color: dt('toggleswitch.handle.color');
        width: dt('toggleswitch.handle.size');
        height: dt('toggleswitch.handle.size');
        inset-inline-start: dt('toggleswitch.gap');
        margin-block-start: calc(-1 * calc(dt('toggleswitch.handle.size') / 2));
        border-radius: dt('toggleswitch.handle.border.radius');
        transition:
            background dt('toggleswitch.transition.duration'),
            color dt('toggleswitch.transition.duration'),
            inset-inline-start dt('toggleswitch.slide.duration'),
            box-shadow dt('toggleswitch.slide.duration');
    }

    .p-toggleswitch.p-toggleswitch-checked .p-toggleswitch-slider {
        background: dt('toggleswitch.checked.background');
        border-color: dt('toggleswitch.checked.border.color');
    }

    .p-toggleswitch.p-toggleswitch-checked .p-toggleswitch-handle {
        background: dt('toggleswitch.handle.checked.background');
        color: dt('toggleswitch.handle.checked.color');
        inset-inline-start: calc(dt('toggleswitch.width') - calc(dt('toggleswitch.handle.size') + dt('toggleswitch.gap')));
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:hover) .p-toggleswitch-slider {
        background: dt('toggleswitch.hover.background');
        border-color: dt('toggleswitch.hover.border.color');
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:hover) .p-toggleswitch-handle {
        background: dt('toggleswitch.handle.hover.background');
        color: dt('toggleswitch.handle.hover.color');
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:hover).p-toggleswitch-checked .p-toggleswitch-slider {
        background: dt('toggleswitch.checked.hover.background');
        border-color: dt('toggleswitch.checked.hover.border.color');
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:hover).p-toggleswitch-checked .p-toggleswitch-handle {
        background: dt('toggleswitch.handle.checked.hover.background');
        color: dt('toggleswitch.handle.checked.hover.color');
    }

    .p-toggleswitch:not(.p-disabled):has(.p-toggleswitch-input:focus-visible) .p-toggleswitch-slider {
        box-shadow: dt('toggleswitch.focus.ring.shadow');
        outline: dt('toggleswitch.focus.ring.width') dt('toggleswitch.focus.ring.style') dt('toggleswitch.focus.ring.color');
        outline-offset: dt('toggleswitch.focus.ring.offset');
    }

    .p-toggleswitch.p-invalid > .p-toggleswitch-slider {
        border-color: dt('toggleswitch.invalid.border.color');
    }

    .p-toggleswitch.p-disabled {
        opacity: 1;
    }

    .p-toggleswitch.p-disabled .p-toggleswitch-slider {
        background: dt('toggleswitch.disabled.background');
    }

    .p-toggleswitch.p-disabled .p-toggleswitch-handle {
        background: dt('toggleswitch.handle.disabled.background');
    }
`;var Pe=["handle"],Ie=["input"],Oe=r=>({checked:r});function Le(r,l){r&1&&R(0)}function Ge(r,l){if(r&1&&G(0,Le,1,0,"ng-container",3),r&2){let o=$();u("ngTemplateOutlet",o.handleTemplate||o._handleTemplate)("ngTemplateOutletContext",J(2,Oe,o.checked()))}}var He=`
    ${Fe}

    p-toggleswitch.ng-invalid.ng-dirty > .p-toggleswitch-slider {
        border-color: dt('toggleswitch.invalid.border.color');
    }
`,qe={root:{position:"relative"}},Re={root:({instance:r})=>["p-toggleswitch p-component",{"p-toggleswitch p-component":!0,"p-toggleswitch-checked":r.checked(),"p-disabled":r.$disabled(),"p-invalid":r.invalid()}],input:"p-toggleswitch-input",slider:"p-toggleswitch-slider",handle:"p-toggleswitch-handle"},Ae=(()=>{class r extends te{name="toggleswitch";style=He;classes=Re;inlineStyles=qe;static \u0275fac=(()=>{let o;return function(e){return(o||(o=D(r)))(e||r)}})();static \u0275prov=V({token:r,factory:r.\u0275fac})}return r})();var Me=new N("TOGGLESWITCH_INSTANCE"),ze={provide:ie,useExisting:M(()=>x),multi:!0},x=(()=>{class r extends we{$pcToggleSwitch=h(Me,{optional:!0,skipSelf:!0})??void 0;bindDirectiveInstance=h(_,{self:!0});onAfterViewChecked(){this.bindDirectiveInstance.setAttrs(this.ptms(["host","root"]))}styleClass;tabindex;inputId;readonly;trueValue=!0;falseValue=!1;ariaLabel;size=X();ariaLabelledBy;autofocus;onChange=new P;input;handleTemplate;_handleTemplate;focused=!1;_componentStyle=h(Ae);templates;onHostClick(o){this.onClick(o)}onAfterContentInit(){this.templates.forEach(o=>{switch(o.getType()){case"handle":this._handleTemplate=o.template;break;default:this._handleTemplate=o.template;break}})}onClick(o){!this.$disabled()&&!this.readonly&&(this.writeModelValue(this.checked()?this.falseValue:this.trueValue),this.onModelChange(this.modelValue()),this.onChange.emit({originalEvent:o,checked:this.modelValue()}),this.input.nativeElement.focus())}onFocus(){this.focused=!0}onBlur(){this.focused=!1,this.onModelTouched()}checked(){return this.modelValue()===this.trueValue}writeControlValue(o,t){t(o),this.cd.markForCheck()}get dataP(){return this.cn({checked:this.checked(),disabled:this.$disabled(),invalid:this.invalid()})}static \u0275fac=(()=>{let o;return function(e){return(o||(o=D(r)))(e||r)}})();static \u0275cmp=w({type:r,selectors:[["p-toggleswitch"],["p-toggleSwitch"],["p-toggle-switch"]],contentQueries:function(t,e,s){if(t&1&&j(s,Pe,4)(s,ee,4),t&2){let p;v(p=E())&&(e.handleTemplate=p.first),v(p=E())&&(e.templates=p)}},viewQuery:function(t,e){if(t&1&&Q(Ie,5),t&2){let s;v(s=E())&&(e.input=s.first)}},hostVars:7,hostBindings:function(t,e){t&1&&c("click",function(p){return e.onHostClick(p)}),t&2&&(f("data-p-checked",e.checked())("data-p-disabled",e.$disabled())("data-p",e.dataP),U(e.sx("root")),b(e.cn(e.cx("root"),e.styleClass)))},inputs:{styleClass:"styleClass",tabindex:[2,"tabindex","tabindex",Y],inputId:"inputId",readonly:[2,"readonly","readonly",F],trueValue:"trueValue",falseValue:"falseValue",ariaLabel:"ariaLabel",size:[1,"size"],ariaLabelledBy:"ariaLabelledBy",autofocus:[2,"autofocus","autofocus",F]},outputs:{onChange:"onChange"},features:[C([ze,Ae,{provide:Me,useExisting:r},{provide:he,useExisting:r}]),O([_]),L],decls:5,vars:22,consts:[["input",""],["type","checkbox","role","switch",3,"focus","blur","checked","pAutoFocus","pBind"],[3,"pBind"],[4,"ngTemplateOutlet","ngTemplateOutletContext"]],template:function(t,e){if(t&1){let s=z();i(0,"input",1,0),c("focus",function(){return k(s),T(e.onFocus())})("blur",function(){return k(s),T(e.onBlur())}),n(),i(2,"div",2)(3,"div",2),H(4,Ge,1,4,"ng-container"),n()()}t&2&&(b(e.cx("input")),u("checked",e.checked())("pAutoFocus",e.autofocus)("pBind",e.ptm("input")),f("id",e.inputId)("required",e.required()?"":void 0)("disabled",e.$disabled()?"":void 0)("aria-checked",e.checked())("aria-labelledby",e.ariaLabelledBy)("aria-label",e.ariaLabel)("name",e.name())("tabindex",e.tabindex),d(2),b(e.cx("slider")),u("pBind",e.ptm("slider")),f("data-p",e.dataP),d(),b(e.cx("handle")),u("pBind",e.ptm("handle")),f("data-p",e.dataP),d(),q(e.handleTemplate||e._handleTemplate?4:-1))},dependencies:[y,Z,_e,S,me,_],encapsulation:2,changeDetection:0})}return r})(),Ve=(()=>{class r{static \u0275fac=function(t){return new(t||r)};static \u0275mod=I({type:r});static \u0275inj=B({imports:[x,S,S]})}return r})();var Be=class r{fb=h(pe);settingsService=h(Se);messageService=h(A);settingForm;cameras=[];isLoading=!1;resolutions=[{label:"\u{1F680} FWVGA (854 x 480) - Si\xEAu m\u01B0\u1EE3t [Khuy\xEAn d\xF9ng Pi 3]",value:"854x480"},{label:"HD (1280 x 720) - 16:9 [Ti\xEAu chu\u1EA9n]",value:"1280x720"},{label:"VGA (640 x 480) - 4:3 [Nh\u1EB9]",value:"640x480"},{label:"SVGA (800 x 600) - 4:3",value:"800x600"},{label:"Full HD (1920 x 1080) - [N\u1EB7ng]",value:"1920x1080"}];aiOptions=[{label:"Th\u1EA5p (0.3) - Nh\u1EA1y, d\u1EC5 b\u1EAFt nh\u1EA7m",value:.3},{label:"Trung b\xECnh (0.5) - Khuy\xEAn d\xF9ng",value:.5},{label:"Cao (0.7) - Ch\xEDnh x\xE1c",value:.7},{label:"R\u1EA5t cao (0.85) - R\u1EA5t ch\u1EB7t ch\u1EBD",value:.85}];timeoutOptions=[{label:"30 gi\xE2y (Nhanh)",value:30},{label:"1 ph\xFAt (Ti\xEAu chu\u1EA9n)",value:60},{label:"2 ph\xFAt",value:120},{label:"5 ph\xFAt",value:300},{label:"10 ph\xFAt",value:600}];fpsOptions=[{label:"10 FPS (T\u1ED1i \u01B0u l\u01B0u tr\u1EEF)",value:10},{label:"15 FPS (M\u01B0\u1EE3t m\xE0)",value:15},{label:"20 FPS (Ti\xEAu chu\u1EA9n)",value:20},{label:"25 FPS (Cao - T\u1ED1n dung l\u01B0\u1EE3ng)",value:25}];fpsViewOptions=[{label:"10 FPS (Ti\u1EBFt ki\u1EC7m CPU)",value:10},{label:"15 FPS (Khuy\xEAn d\xF9ng)",value:15},{label:"20 FPS (M\u01B0\u1EE3t)",value:20},{label:"25 FPS (R\u1EA5t m\u01B0\u1EE3t - T\u1ED1n CPU)",value:25}];constructor(){this.settingForm=this.fb.group({save_media:["app/media",g.required],resolution:["854x480",g.required],ai_confidence:[.5,g.required],timeout_no_human:[60,g.required],work_end_time:["18:30",g.required],read_end_order:[5,g.required],perf_record_fps:[10,g.required],perf_view_fps:[15,g.required],perf_ai_interval:[12,g.required],enable_audio:[!1]})}ngOnInit(){this.loadData()}loadData(){this.isLoading=!0,this.settingsService.getCameras().subscribe({next:l=>this.cameras=l,error:()=>console.warn("Kh\xF4ng t\u1EA3i \u0111\u01B0\u1EE3c danh s\xE1ch camera")}),this.settingsService.getSettings().subscribe({next:l=>{let o=l.camera_width||854,t=l.camera_height||480,e=`${o}x${t}`;this.resolutions.some(p=>p.value===e)||this.resolutions.push({label:`T\xF9y ch\u1EC9nh (${o} x ${t})`,value:e}),this.settingForm.patchValue({save_media:l.save_media||"app/media",resolution:e,ai_confidence:Number(l.ai_confidence)||.5,timeout_no_human:Number(l.timeout_no_human)||60,work_end_time:l.work_end_time||"18:30",read_end_order:Number(l.read_end_order)||5,perf_record_fps:Number(l.perf_record_fps)||10,perf_view_fps:Number(l.perf_view_fps)||15,perf_ai_interval:Number(l.perf_ai_interval)||12,enable_audio:String(l.enable_audio).toLowerCase()==="true"}),this.isLoading=!1},error:l=>{this.messageService.add({severity:"error",summary:"L\u1ED7i",detail:"Kh\xF4ng t\u1EA3i \u0111\u01B0\u1EE3c c\u1EA5u h\xECnh t\u1EEB Server"}),this.isLoading=!1}})}saveSettings(){if(this.settingForm.invalid){this.messageService.add({severity:"warn",summary:"C\u1EA3nh b\xE1o",detail:"Vui l\xF2ng \u0111i\u1EC1n \u0111\u1EA7y \u0111\u1EE7 th\xF4ng tin"});return}this.isLoading=!0;let l=this.settingForm.value,[o,t]=l.resolution.split("x"),e={save_media:l.save_media,camera_width:String(o),camera_height:String(t),ai_confidence:String(l.ai_confidence),timeout_no_human:String(l.timeout_no_human),work_end_time:String(l.work_end_time),read_end_order:String(l.read_end_order),perf_record_fps:String(l.perf_record_fps),perf_view_fps:String(l.perf_view_fps),perf_ai_interval:String(l.perf_ai_interval),enable_audio:l.enable_audio?"true":"false"};console.log("\u{1F680} Sending Payload:",e),this.settingsService.updateSettings(e).subscribe({next:s=>{this.messageService.add({severity:"success",summary:"Th\xE0nh c\xF4ng",detail:"\u0110\xE3 l\u01B0u c\u1EA5u h\xECnh. \u0110ang kh\u1EDFi \u0111\u1ED9ng l\u1EA1i d\u1ECBch v\u1EE5...",life:4e3}),this.isLoading=!1},error:s=>{console.error("\u274C Save Error:",s),this.messageService.add({severity:"error",summary:"L\u1ED7i",detail:"Kh\xF4ng th\u1EC3 l\u01B0u c\u1EA5u h\xECnh xu\u1ED1ng Database"}),this.isLoading=!1}})}static \u0275fac=function(o){return new(o||r)};static \u0275cmp=w({type:r,selectors:[["app-settings"]],features:[C([A])],decls:84,vars:12,consts:[[1,"surface-section","p-4","md:p-6","lg:p-8"],[1,"grid","grid-cols-1","md:grid-cols-2","xl:grid-cols-3","gap-4","max-w-full","mx-auto","pb-8"],[1,"col-span-1"],["header","\u2699\uFE0F Camera & H\xECnh \u1EA3nh","styleClass","h-full shadow-md"],[1,"flex","flex-col","gap-5",3,"formGroup"],[1,"flex","flex-col","gap-2"],[1,"font-bold","text-gray-700"],["formControlName","resolution","optionLabel","label","optionValue","value","placeholder","Ch\u1ECDn \u0111\u1ED9 ph\xE2n gi\u1EA3i","styleClass","w-full",3,"onChange","options"],[1,"text-blue-500"],[1,"pi","pi-info-circle"],["pInputText","","formControlName","save_media","placeholder","app/media",1,"w-full",3,"blur"],[1,"text-gray-500"],["header","\u{1F916} V\u1EADn h\xE0nh & AI","styleClass","h-full shadow-md"],["formControlName","timeout_no_human","optionLabel","label","optionValue","value","placeholder","Ch\u1ECDn th\u1EDDi gian ch\u1EDD","styleClass","w-full",3,"onChange","options"],[1,"flex","align-items-center","gap-3"],["formControlName","enable_audio",3,"onChange"],[1,"text-gray-600","font-medium"],["formControlName","ai_confidence","optionLabel","label","optionValue","value","placeholder","Ch\u1ECDn \u0111\u1ED9 nh\u1EA1y","styleClass","w-full",3,"onChange","options"],[1,"flex","align-items-center","gap-2"],["pInputText","","type","number","formControlName","read_end_order","min","3","max","10",1,"w-4rem"],[1,"text-gray-600"],["pInputText","","type","time","formControlName","work_end_time",1,"w-full",3,"change"],["header","\u{1F680} T\u1ED1i \u01B0u Hi\u1EC7u n\u0103ng (Orange Pi)","styleClass","h-full shadow-md surface-50 border-blue-100 border-1"],[1,"font-bold","text-red-600"],["formControlName","perf_record_fps","optionLabel","label","optionValue","value","styleClass","w-full",3,"onChange","options"],[1,"font-bold","text-blue-600"],["formControlName","perf_view_fps","optionLabel","label","optionValue","value","styleClass","w-full",3,"onChange","options"],[1,"font-bold","text-purple-600"],[1,"font-bold"],["pInputText","","type","number","formControlName","perf_ai_interval","min","1","max","30",1,"w-5rem","text-center"],[1,"fixed","bottom-0","left-0","w-full","bg-white","border-t","border-gray-200","p-3","flex","justify-center","z-50","shadow-lg"],["label","L\u01B0u T\u1EA5t C\u1EA3 C\u1EA5u H\xECnh","icon","pi pi-save","styleClass","p-button-primary px-6 p-button-rounded font-bold",3,"onClick","loading"]],template:function(o,t){if(o&1&&(m(0,"p-toast"),i(1,"div",0)(2,"div",1)(3,"div",2)(4,"p-card",3)(5,"form",4)(6,"div",5)(7,"label",6),a(8,"\u0110\u1ED9 ph\xE2n gi\u1EA3i (Resolution)"),n(),i(9,"p-select",7),c("onChange",function(){return t.saveSettings()}),n(),i(10,"small",8),m(11,"i",9),a(12," 854x480 l\xE0 m\u1EE9c m\u01B0\u1EE3t nh\u1EA5t cho Orange Pi 3."),n()(),i(13,"div",5)(14,"label",6),a(15,"Th\u01B0 m\u1EE5c l\u01B0u tr\u1EEF"),n(),i(16,"input",10),c("blur",function(){return t.saveSettings()}),n(),i(17,"small",11),a(18,"N\u01A1i l\u01B0u Video/\u1EA2nh tr\xEAn th\u1EBB nh\u1EDB."),n()()()()(),i(19,"div",2)(20,"p-card",12)(21,"form",4)(22,"div",5)(23,"label",6),a(24,"Timeout (T\u1EF1 ng\u1EAFt)"),n(),i(25,"p-select",13),c("onChange",function(){return t.saveSettings()}),n(),i(26,"small",11),a(27,"T\u1EF1 \u0111\xF3ng \u0111\u01A1n n\u1EBFu Camera kh\xF4ng th\u1EA5y ng\u01B0\u1EDDi."),n()(),i(28,"div",5)(29,"label",6),a(30,"Tr\u1EE3 l\xFD Gi\u1ECDng n\xF3i (TTS)"),n(),i(31,"div",14)(32,"p-toggleswitch",15),c("onChange",function(){return t.saveSettings()}),n(),i(33,"span",16),a(34),n()(),i(35,"small",11),a(36,"T\u1EAFt \u0111i n\u1EBFu ch\u01B0a c\xE0i driver \xE2m thanh \u0111\u1EC3 tr\xE1nh l\u1ED7i."),n()(),i(37,"div",5)(38,"label",6),a(39,"\u0110\u1ED9 nh\u1EA1y AI (Confidence)"),n(),i(40,"p-select",17),c("onChange",function(){return t.saveSettings()}),n()(),i(41,"div",5)(42,"label",6),a(43,"\u0110\u1ECDc s\u1ED1 cu\u1ED1i m\xE3 \u0111\u01A1n (TTS)"),n(),i(44,"div",18),m(45,"input",19),i(46,"span",20),a(47,"s\u1ED1 cu\u1ED1i"),n()(),i(48,"small",11),a(49,'V\xED d\u1EE5: M\xE3 ...8829 -> \u0110\u1ECDc "Hai ch\xEDn".'),n()(),i(50,"div",5)(51,"label",6),a(52,"Gi\u1EDD k\u1EBFt th\xFAc ca"),n(),i(53,"input",21),c("change",function(){return t.saveSettings()}),n()()()()(),i(54,"div",2)(55,"p-card",22)(56,"form",4)(57,"div",5)(58,"label",23),a(59,"FPS Ghi h\xECnh (Record)"),n(),i(60,"p-select",24),c("onChange",function(){return t.saveSettings()}),n(),i(61,"small",11),a(62,"Th\u1EA5p (10-12) gi\xFAp CPU kh\xF4ng b\u1ECB qu\xE1 t\u1EA3i khi n\xE9n video."),n()(),i(63,"div",5)(64,"label",25),a(65,"FPS Hi\u1EC3n th\u1ECB (View)"),n(),i(66,"p-select",26),c("onChange",function(){return t.saveSettings()}),n(),i(67,"small",11),a(68,"Gi\u1EDBi h\u1EA1n t\u1ED1c \u0111\u1ED9 x\u1EED l\xFD \u1EA3nh \u0111\u1EC3 m\xE1y m\xE1t h\u01A1n."),n()(),i(69,"div",5)(70,"label",27),a(71,"T\u1EA7n su\u1EA5t AI (Interval)"),n(),i(72,"div",18)(73,"span",28),a(74,"M\u1ED7i"),n(),m(75,"input",29),i(76,"span",28),a(77,"frame qu\xE9t 1 l\u1EA7n"),n()(),i(78,"small",11),a(79," T\u0103ng s\u1ED1 n\xE0y l\xEAn (vd: 12, 15) n\u1EBFu m\xE1y b\u1ECB lag. "),m(80,"br"),a(81,"12 = Qu\xE9t 2 l\u1EA7n/gi\xE2y. "),n()()()()()(),i(82,"div",30)(83,"p-button",31),c("onClick",function(){return t.saveSettings()}),n()()()),o&2){let e,s;d(5),u("formGroup",t.settingForm),d(4),u("options",t.resolutions),d(12),u("formGroup",t.settingForm),d(4),u("options",t.timeoutOptions),d(8),K("text-green-600",(e=t.settingForm.get("enable_audio"))==null?null:e.value),d(),W(" ",(s=t.settingForm.get("enable_audio"))!=null&&s.value?"\u0110ang B\u1EACT \u{1F50A}":"\u0110ang T\u1EAET \u{1F507}"," "),d(6),u("options",t.aiOptions),d(16),u("formGroup",t.settingForm),d(4),u("options",t.fpsOptions),d(6),u("options",t.fpsViewOptions),d(17),u("loading",t.isLoading)}},dependencies:[y,ge,le,ne,ae,oe,re,ce,ue,de,se,ke,xe,ye,Ce,Ee,ve,be,fe,De,Te,Ve,x],styles:['@charset "UTF-8";.surface-section[_ngcontent-%COMP%]{background-color:#f8fafc;min-height:100vh}  .p-card{border:none;box-shadow:0 4px 6px -1px #0000001a,0 2px 4px -1px #0000000f;border-radius:.75rem;background:#fff;transition:transform .2s ease-in-out,box-shadow .2s ease-in-out}  .p-card:hover{box-shadow:0 10px 15px -3px #0000001a,0 4px 6px -2px #0000000d}  .p-card .p-card-header{padding:1.5rem 1.5rem .5rem;font-size:1.1rem;font-weight:600;color:#334155;border-bottom:1px solid #f1f5f9;margin-bottom:1rem}  .p-card .p-card-body{padding:1.5rem}label[_ngcontent-%COMP%]{display:block;margin-bottom:.5rem;color:#475569;font-weight:500;font-size:.95rem}small[_ngcontent-%COMP%]{display:block;margin-top:.35rem;color:#94a3b8;font-size:.85rem}  .p-inputtext,   .p-inputnumber-input{width:100%;padding:.75rem 1rem;border-radius:.5rem;border:1px solid #cbd5e1;background-color:#f8fafc;transition:border-color .2s,background-color .2s}  .p-inputtext:hover,   .p-inputnumber-input:hover{border-color:#94a3b8}  .p-inputtext:focus,   .p-inputnumber-input:focus{border-color:#3b82f6;background-color:#fff;box-shadow:0 0 0 2px #3b82f633}.grid[_ngcontent-%COMP%]{display:grid;grid-template-columns:repeat(1,minmax(0,1fr));gap:1.5rem}@media(min-width:768px){.grid[_ngcontent-%COMP%]{grid-template-columns:repeat(2,minmax(0,1fr))}}.col-span-1[_ngcontent-%COMP%]{grid-column:span 1/span 1}.flex-col[_ngcontent-%COMP%]{display:flex;flex-direction:column}.gap-1[_ngcontent-%COMP%]{gap:.25rem}.gap-4[_ngcontent-%COMP%]{gap:1.5rem}.fixed-footer[_ngcontent-%COMP%]{position:fixed;bottom:0;left:0;right:0;background-color:#ffffffe6;-webkit-backdrop-filter:blur(8px);backdrop-filter:blur(8px);padding:1rem 2rem;border-top:1px solid #e2e8f0;display:flex;justify-content:flex-end;z-index:100;box-shadow:0 -4px 6px -1px #0000000d}[_nghost-%COMP%]{display:block;padding-bottom:5rem}']})};export{Be as SettingsComponent};
