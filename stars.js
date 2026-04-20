// Shared stars canvas animation
(function(){
  const c = document.getElementById('stars');
  if(!c) return;
  const ctx = c.getContext('2d');
  let S = [];
  const N = 180;
  function resize(){
    c.width = window.innerWidth;
    c.height = Math.max(document.documentElement.scrollHeight, window.innerHeight);
    S = [];
    for(let i=0;i<N;i++) S.push({
      x:Math.random()*c.width, y:Math.random()*c.height,
      r:Math.random()*1.1+0.2, a:Math.random()*0.4+0.08,
      p:Math.random()*0.018+0.004, ph:Math.random()*Math.PI*2
    });
  }
  let f=0;
  function draw(){
    ctx.clearRect(0,0,c.width,c.height);
    f++;
    const palette=[
      [197,184,222],[155,138,191],[0,181,160],[74,112,181],[123,80,163],[214,74,140]
    ];
    S.forEach((s,i)=>{
      const a=s.a+Math.sin(f*s.p+s.ph)*0.12;
      const c2=palette[i%palette.length];
      ctx.beginPath();
      ctx.arc(s.x,s.y,s.r,0,Math.PI*2);
      ctx.fillStyle=`rgba(${c2[0]},${c2[1]},${c2[2]},${Math.max(0,a)})`;
      ctx.fill();
    });
    requestAnimationFrame(draw);
  }
  resize(); draw();
  window.addEventListener('resize',resize);
  window.addEventListener('load',resize);
  new ResizeObserver(resize).observe(document.body);
})();

// Nav scroll
const nav=document.getElementById('nav');
if(nav) window.addEventListener('scroll',()=>nav.classList.toggle('scrolled',scrollY>50));

// Fade in
const obs=new IntersectionObserver(e=>e.forEach(x=>{if(x.isIntersecting)x.target.classList.add('v')}),{threshold:0.1,rootMargin:'0px 0px -30px 0px'});
document.querySelectorAll('.fi').forEach(el=>obs.observe(el));

// Mobile menu
const toggle=document.getElementById('navToggle');
const links=document.getElementById('navLinks');
if(toggle&&links){
  toggle.addEventListener('click',()=>links.classList.toggle('open'));
  links.querySelectorAll('a').forEach(a=>a.addEventListener('click',()=>links.classList.remove('open')));
}
