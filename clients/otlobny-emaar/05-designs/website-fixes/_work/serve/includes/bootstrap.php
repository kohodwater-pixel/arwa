<?php
// TEST STUB ONLY — not part of the delivery. Stands in for the real includes/bootstrap.php,
// which the agency does not have. Rows use titles and texts read from the live site crawl (2026-11-27).
// STUB_SETTINGS=defaults : settings() returns no name/meta keys, so the code defaults show.
// STUB_SETTINGS=live     : settings() returns the values the live database holds today (old name).
function is_installed(){return true;}
function redirect($to){header('Location: '.$to,true,302);exit;}
function e($v){return htmlspecialchars((string)$v,ENT_QUOTES|ENT_SUBSTITUTE,'UTF-8');}
function base_url($path=''){return '/'.ltrim((string)$path,'/');}
function media_url($path){$path=(string)$path;if($path==='')return '';if(preg_match('#^https?://#i',$path))return $path;return '/'.ltrim($path,'/');}
function csrf_field(){return '<input type="hidden" name="csrf" value="stub-csrf-token">';}
function settings(){
    $base=['theme'=>'dark','logo_path'=>'assets/images/logo-test.svg','contact_email'=>'info@otlobny.co','whatsapp'=>'+966549555514'];
    if((getenv('STUB_SETTINGS')?:'defaults')==='live'){
        $base+=['site_name'=>'أطلبني للتشغيل والصيانة','meta_title'=>'أطلبني | للصيانة والنظافة والتشغيل','meta_description'=>'خدمات صيانة ونظافة وتشغيل وضيافة وكوادر متخصصة للمنشآت.','site_description'=>'تشغيل بلا تعقيد.. وجاهزية بلا توقف'];
    }
    return $base;
}
function stub_services(){
    $j=fn($a)=>json_encode($a,JSON_UNESCAPED_UNICODE);
    return [
        ['slug'=>'maintenance','title'=>'أعمال الصيانة','eyebrow'=>'جاهزية مستمرة','short_description'=>'حلول صيانة تحافظ على كفاءة مرافقك.','full_description'=>'ننفذ أعمال الصيانة الوقائية والتصحيحية بما يرفع جاهزية منشأتك ويقلل توقف الأعمال.','benefits_json'=>$j(['خطط مرنة حسب الموقع','فنيون مؤهلون','متابعة منظمة']),'steps_json'=>$j(['فهم الموقع','تحديد النطاق','تنفيذ ومتابعة'])],
        ['slug'=>'cleaning','title'=>'أعمال النظافة والضيافة','eyebrow'=>'بيئة تليق بمنشأتك','short_description'=>'خدمات نظافة وضيافة منظمة للمنشآت.','full_description'=>'نوفر بيئة نظيفة ومنظمة عبر خطط تشغيل تناسب المنشآت الحكومية والخاصة والتجارية.','benefits_json'=>$j(['فرق مدربة','خطط نظافة دورية','إشراف مستمر']),'steps_json'=>$j(['معاينة الاحتياج','تجهيز الفريق','متابعة الجودة'])],
        ['slug'=>'contracting','title'=>'المقاولات العامة','eyebrow'=>'تنفيذ مدروس','short_description'=>'أعمال ترميم وإنشاء وكهرباء وميكانيكا.','full_description'=>'ندير نطاق الأعمال من الدراسة إلى التنفيذ في أعمال المقاولات والترميم والتشطيبات والخدمات الفنية.','benefits_json'=>$j(['نطاق واضح','تنسيق فني','تنفيذ منظم']),'steps_json'=>$j(['دراسة المشروع','خطة التنفيذ','تسليم الأعمال'])],
        ['slug'=>'workforce','title'=>'تأمين الكوادر','eyebrow'=>'الفريق المناسب','short_description'=>'كوادر تشغيل وخدمة تناسب احتياج منشأتك.','full_description'=>'نوفر كوادر نظامية ومؤهلة للتشغيل والضيافة والخدمات وفق متطلبات العمل.','benefits_json'=>$j(['اختيار مناسب','مرونة تشغيلية','متابعة الاحتياج']),'steps_json'=>$j(['تحديد المتطلبات','ترشيح الكوادر','بدء التشغيل'])],
    ];
}
function active_services(){return stub_services();}
function service_by_slug($slug){foreach(stub_services() as $r)if($r['slug']===$slug)return $r;return null;}
function active_faqs(){return [
    ['question'=>'ما الخدمات التي تقدمها أطلبني؟','answer'=>'نقدم أعمال الصيانة والنظافة والضيافة والمقاولات العامة وتأمين الكوادر.'],
    ['question'=>'كيف أطلب عرض سعر؟','answer'=>'اختر الخدمة المناسبة ثم أرسل تفاصيل منشأتك من نموذج طلب عرض السعر.'],
    ['question'=>'هل يمكن تعديل نطاق الخدمة؟','answer'=>'نعم، يتم تحديد نطاق العمل وفق احتياج المنشأة وطبيعة الموقع.'],
    ['question'=>'هل يمكن التواصل عبر واتساب؟','answer'=>'نعم، يمكنك التواصل عبر رقم واتساب أطلبني الظاهر في الموقع.'],
];}
function active_projects(){return [
    ['title'=>'فريق نظافة محترف','service_slug'=>'cleaning','image_path'=>'assets/images/project-01.png','description'=>'كوادر مدرّبة تعكس هوية أطلبني داخل المنشآت.'],
    ['title'=>'تشغيل نظافة متكامل','service_slug'=>'cleaning','image_path'=>'assets/images/project-02.png','description'=>'تنفيذ منظم للاهتمام بأدق تفاصيل بيئة العمل.'],
    ['title'=>'صف اختبار: معرّف خدمة غير موجود','service_slug'=>'no-such-slug','image_path'=>'','description'=>'صف للاختبار فقط للتأكد من النص البديل «خدمات اطلبني».'],
];}
function active_partners(){$out=[];for($i=1;$i<=16;$i++)$out[]=['name'=>'شريك نجاح','logo_path'=>sprintf('uploads/images/partner-%02d.jpg',$i),'website_url'=>''];return $out;}
