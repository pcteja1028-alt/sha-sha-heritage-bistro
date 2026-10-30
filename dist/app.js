import * as THREE from 'three';
import { GLTFLoader } from './vendor/GLTFLoader.js';
import { DRACOLoader } from './vendor/DRACOLoader.js';
import { RoomEnvironment } from './vendor/RoomEnvironment.js';
const $=s=>document.querySelector(s), canvas=$('#scene'), container=$('.experience');
let renderView=true;
function showRender(on){renderView=on;container.classList.toggle('render-view',on);$('#view-mode').textContent=on?'Explore in 3D':'View final render';$('#view-mode').setAttribute('aria-pressed',String(on));}
showRender(true);$('#view-mode').onclick=()=>showRender(!renderView);
const scene=new THREE.Scene();scene.background=new THREE.Color('#c3b7a3');
const camera=new THREE.PerspectiveCamera(53,1,.04,100);camera.rotation.order='YXZ';
let renderer;try{renderer=new THREE.WebGLRenderer({canvas,antialias:true,powerPreference:'high-performance'});}catch(e){$('#loading').innerHTML='<strong>3D graphics unavailable</strong><small>Enable hardware acceleration in your browser, then reload.</small>';throw e;}
renderer.setPixelRatio(Math.min(devicePixelRatio,2));renderer.outputColorSpace=THREE.SRGBColorSpace;renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=.8;renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
const pmrem=new THREE.PMREMGenerator(renderer);scene.environment=pmrem.fromScene(new RoomEnvironment(),.04).texture;scene.environmentIntensity=.3;pmrem.dispose();
const hemi=new THREE.HemisphereLight(0xffe9cc,0x6b5540,.3);scene.add(hemi);
const sun=new THREE.DirectionalLight(0xffdeb0,.4);sun.position.set(-3,7,5);scene.add(sun);
for(const z of [3,7,12]){const l=new THREE.SpotLight(0xffdeb0,8,8,1.1,.7,1.5);l.position.set(0,2.85,-z*.74);l.target.position.set(0,0,-z*.74);l.castShadow=true;l.shadow.mapSize.set(1024,1024);l.shadow.bias=-.0004;scene.add(l,l.target);}
const interior=[];for(let z of [1.4,3.6,5.8,8,10.3,12.5]){let l=new THREE.PointLight(0xffdfb0,3,5,2);l.position.set(0,2.4,-z*.74);scene.add(l);interior.push(l);}
// Blender uses Z up; glTF converts to Y up and negative Z depth.
const stops=[
 {title:'The arrival.',description:'A warm walnut frame and quiet brass lettering welcome you inside.',p:[0,1.75,3.8],t:[0,1.55,-2]},
 {title:'A warm welcome.',description:'The long sightline draws you through the room, from the entrance to the open kitchen.',p:[.67,1.58,-.38],t:[-.15,1.45,-7]},
 {title:'Stay a little longer.',description:'Cognac channel seating, cream stone tables and the soft glow of opal globes.',p:[.72,1.65,-4.1],t:[-1.05,1.05,-5.9]},
 {title:'Craft on display.',description:'A walnut and cream counter frames the ingredients, with a working passage to the right.',p:[.68,1.65,-7.85],t:[-.4,1.25,-9.3]},
 {title:'Behind the experience.',description:'Preparation and cold storage lead to the shawarma, griddle, fryer, round cooker and sink.',p:[.42,1.7,-11.9],t:[0,1.42,-13.05]}
];
for(const stop of stops){if(stop.p[2]<0)stop.p[2]*=.74;if(stop.t[2]<0)stop.t[2]*=.74;}
let model,selected=1,transition=null,touring=false,tourAt=0,cutaway=false,day=false,drag=null,yaw=0,pitch=0,keys=new Set(),ready=false;
const hidden=[];const reduced=matchMedia('(prefers-reduced-motion: reduce)').matches;
function finishMaterials(root){root.traverse(o=>{if(!o.isMesh)return;for(const m of (Array.isArray(o.material)?o.material:[o.material])){if(m.map)m.map.anisotropy=renderer.capabilities.getMaxAnisotropy();if(m.name.includes('brass'))m.envMapIntensity=1.2;}});}
function syncAngles(){const e=new THREE.Euler().setFromQuaternion(camera.quaternion,'YXZ');yaw=e.y;pitch=e.x;}
function moveTo(p,t,duration=1800){const dest=new THREE.Vector3(...p),dummy=new THREE.PerspectiveCamera();dummy.position.copy(dest);dummy.lookAt(...t);transition={start:performance.now(),duration:reduced?0:duration,from:camera.position.clone(),to:dest,q0:camera.quaternion.clone(),q1:dummy.quaternion.clone()};}
function stopTour(){touring=false;$('#tour').textContent='▶ Guided tour';}
function setCut(on){cutaway=on;renderer.clippingPlanes=on?[new THREE.Plane(new THREE.Vector3(0,-1,0),2.7),new THREE.Plane(new THREE.Vector3(-1,0,0),1.35)]:[];$('#cut').setAttribute('aria-pressed',String(on));}
function go(i,auto=false){if(!ready)return;showRender(false);if(!auto)stopTour();setCut(false);selected=i;const s=stops[i];moveTo(s.p,s.t);$('#title').textContent=s.title;$('#description').textContent=s.description;$('#number').textContent=`0${i+1} / 05`;$('.stops').querySelectorAll('button').forEach((b,n)=>{b.classList.toggle('active',n===i);b.setAttribute('aria-current',n===i?'step':'false');});$('#marker').style.bottom=[2,9,36,65,88][i]+'%';tourAt=performance.now();}
camera.position.set(...stops[1].p);camera.lookAt(...stops[1].t);syncAngles();
new GLTFLoader().setDRACOLoader(new DRACOLoader().setDecoderPath('./vendor/draco/')).load('./assets/heritage-a01.glb',g=>{model=g.scene;finishMaterials(model);scene.add(model);model.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;if(o.name.startsWith('Ceiling')||o.name.startsWith('Wall_shell')||o.name.startsWith('Rear_wall'))hidden.push(o);if(o.material){o.material.side=THREE.DoubleSide;}}});ready=true;$('#loading').style.display='none';const keepRenderView=renderView;go(1);showRender(keepRenderView);window.walkthrough={scene,camera,model,go,getState:()=>({selected,cutaway,touring,ready,meshes:renderer.info.render.calls})};},undefined,e=>{$('#loading').innerHTML='<strong>The model could not load</strong><small>Please reload this page to try again.</small>';console.error(e);});
document.querySelectorAll('[data-stop]').forEach(b=>b.onclick=()=>go(Number(b.dataset.stop)));
$('#reset').onclick=()=>go(selected);
$('#tour').onclick=()=>{if(touring){stopTour();return;}touring=true;$('#tour').textContent='Ⅱ Pause tour';go(0,true);};
$('#cut').onclick=()=>{if(!ready)return;showRender(false);stopTour();setCut(!cutaway);if(cutaway){moveTo([9,12,6],[0,0,-4.81],2000);$('#title').textContent='The complete picture.';$('#description').textContent='An open-roof view of the A01 concept. Select any section to step back inside.';}else go(selected);};
$('#light').onclick=()=>{day=!day;$('#light').setAttribute('aria-pressed',String(day));$('#light').textContent=day?'◐ Warm mood':'◐ Gallery light';hemi.intensity=day?.6:.3;sun.intensity=day?.8:.4;interior.forEach(l=>l.intensity=day?2:3);renderer.toneMappingExposure=day?1:.8;scene.background.set(day?'#dcd4c5':'#c3b7a3');};
$('#full').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await container.requestFullscreen();}catch{ $('#full').textContent='Unavailable';}};
function dialog(id){$(id).showModal();stopTour();keys.clear();}$('#about').onclick=()=>dialog('#notes');$('#reference').onclick=()=>dialog('#ref');document.querySelectorAll('.close').forEach(b=>b.onclick=()=>b.closest('dialog').close());
canvas.addEventListener('pointerdown',e=>{if(!ready)return;stopTour();transition=null;syncAngles();drag={x:e.clientX,y:e.clientY};canvas.setPointerCapture(e.pointerId);canvas.focus();});
canvas.addEventListener('pointermove',e=>{if(!drag)return;yaw-=(e.clientX-drag.x)*.003;pitch=Math.max(-1.2,Math.min(1.2,pitch-(e.clientY-drag.y)*.003));camera.rotation.set(pitch,yaw,0,'YXZ');drag={x:e.clientX,y:e.clientY};});
canvas.addEventListener('pointerup',()=>drag=null);canvas.addEventListener('pointercancel',()=>drag=null);
const moveKeys=['w','a','s','d','arrowup','arrowdown','arrowleft','arrowright'];window.addEventListener('keydown',e=>{if(document.querySelector('dialog[open]'))return;const k=e.key.toLowerCase();if(moveKeys.includes(k)){e.preventDefault();keys.add(k);stopTour();transition=null;}});window.addEventListener('keyup',e=>keys.delete(e.key.toLowerCase()));window.addEventListener('blur',()=>{keys.clear();drag=null;});
for(const [id,key] of [['forward','w'],['back','s']]){$('#'+id).addEventListener('pointerdown',e=>{stopTour();transition=null;keys.add(key);e.target.setPointerCapture(e.pointerId);});for(const event of ['pointerup','pointercancel','lostpointercapture'])$('#'+id).addEventListener(event,()=>keys.delete(key));}
function walk(dt){if(!keys.size||cutaway||!ready)return;let f=Number(keys.has('w')||keys.has('arrowup'))-Number(keys.has('s')||keys.has('arrowdown')),r=Number(keys.has('d')||keys.has('arrowright'))-Number(keys.has('a')||keys.has('arrowleft'));let v=new THREE.Vector3(r,0,-f);if(v.lengthSq())v.normalize().applyAxisAngle(new THREE.Vector3(0,1,0),camera.rotation.y).multiplyScalar(dt*1.35);const next=camera.position.clone().add(v);next.z=THREE.MathUtils.clamp(next.z,-8.97,4);next.y=1.65;let low=-1.2,high=1.2;if(next.z<-.2&&next.z>-6.29){low=.28;high=1.04;}if(next.z<=-6.29&&next.z>=-7.14){low=.86;high=1.20;}if(next.z<-7.14){low=-.60;high=.62;}next.x=THREE.MathUtils.clamp(next.x,low,high);camera.position.copy(next);$('#marker').style.bottom=THREE.MathUtils.clamp(-next.z/9.92*100,2,94)+'%';}
const resize=()=>{const w=container.clientWidth,h=container.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;camera.updateProjectionMatrix();};new ResizeObserver(resize).observe(container);resize();
let last=performance.now();function animate(now){requestAnimationFrame(animate);const dt=Math.min((now-last)/1000,.04);last=now;if(transition){let a=transition.duration?Math.min(1,(now-transition.start)/transition.duration):1;a=a*a*(3-2*a);camera.position.lerpVectors(transition.from,transition.to,a);camera.quaternion.slerpQuaternions(transition.q0,transition.q1,a);if(a>=1){transition=null;syncAngles();}}walk(dt);if(touring&&now-tourAt>6500){if(selected===4)stopTour();else go(selected+1,true);}if(!renderView)renderer.render(scene,camera);}requestAnimationFrame(animate);


