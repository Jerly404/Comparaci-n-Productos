"use strict";
const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
const FALLBACK="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='240' height='180' viewBox='0 0 240 180'%3E%3Crect width='240' height='180' fill='%23f4f5f8'/%3E%3Cpath d='M93 65h54v50H93z' fill='none' stroke='%23b7becc' stroke-width='3'/%3E%3Cpath d='m96 106 16-17 12 12 8-8 12 13' fill='none' stroke='%23b7becc' stroke-width='3'/%3E%3Ccircle cx='134' cy='79' r='5' fill='%23b7becc'/%3E%3C/svg%3E";
const state={stores:[],selected:new Set(),results:[],stats:{},breakdown:{},favorites:read("comparaya_favorites",[]),compare:[],controller:null};
function read(key,fallback){try{return JSON.parse(localStorage.getItem(key))||fallback}catch{return fallback}}
function save(){localStorage.setItem("comparaya_favorites",JSON.stringify(state.favorites));updateFavoriteCount()}
function esc(v=""){return String(v).replace(/[&<>'"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","'":"&#39;",'"':"&quot;"}[c]))}
function money(v){return new Intl.NumberFormat("es-PE",{style:"currency",currency:"PEN",minimumFractionDigits:2}).format(Number(v)||0).replace("PEN","S/")}
function safeUrl(v){try{const u=new URL(v);return /^https?:$/.test(u.protocol)?u.href:"#"}catch{return "#"}}
function productKey(p){return `${p.store_id}:${p.id||p.url}`}
function isFavorite(p){return state.favorites.some(x=>productKey(x)===productKey(p))}
function imageTag(p,cls=""){const url=p.image_url?safeUrl(p.image_url):FALLBACK;const src=url==="#"?FALLBACK:url;return `<img class="${cls}" src="${esc(src)}" alt="${esc(p.title)}" loading="lazy" onerror="this.onerror=null;this.src='${FALLBACK}'">`}

document.addEventListener("DOMContentLoaded",async()=>{bind();updateFavoriteCount();await loadStores();const q=new URLSearchParams(location.search).get("q");if(q){$("#search-input").value=q;search()}});
async function loadStores(){try{const r=await fetch("/api/stores");if(!r.ok)throw 0;state.stores=await r.json();state.selected=new Set(state.stores.map(s=>s.id));$("#store-count").textContent=state.stores.length;renderStores()}catch{$("#store-filters").innerHTML='<span class="muted">No se pudieron cargar.</span>'}}
function renderStores(){const box=$("#store-filters");box.innerHTML=state.stores.map(s=>`<label class="store-option"><input type="checkbox" value="${esc(s.id)}" ${state.selected.has(s.id)?"checked":""}><i class="store-dot" style="background:${esc(s.color)}"></i>${esc(s.name)}</label>`).join("");box.onchange=e=>{if(!e.target.matches("input"))return;e.target.checked?state.selected.add(e.target.value):state.selected.delete(e.target.value);runIfQuery()};$("#stores-toggle").textContent=state.selected.size?"Desmarcar todas":"Seleccionar todas"}
function bind(){
  $("#search-form").onsubmit=e=>{e.preventDefault();search()};
  $$("[data-query]").forEach(b=>b.onclick=()=>{$("#search-input").value=b.dataset.query;search()});
  $("#sort-select").onchange=search;$("#location-select").onchange=runIfQuery;
  ["#discount-only","#hide-accessories","#include-refurbished"].forEach(id=>$(id).onchange=runIfQuery);
  $("#filters-reset").onclick=resetFilters;$("#empty-retry").onclick=()=>{resetFilters();search()};
  $("#stores-toggle").onclick=()=>{state.selected.size?state.selected.clear():state.stores.forEach(s=>state.selected.add(s.id));renderStores();runIfQuery()};
  $("#mobile-filter").onclick=()=>$("#filters").classList.toggle("open");
  $("#export-button").onclick=exportCsv;$("#favorites-open").onclick=()=>openModal("favorites");
  $("#favorites-clear").onclick=()=>{state.favorites=[];save();renderFavorites();renderResults()};
  $("#compare-open").onclick=()=>openModal("compare");$("#compare-clear").onclick=()=>{state.compare=[];updateCompare();renderResults()};
  $$('[data-close]').forEach(b=>b.onclick=closeModals);$("#modal-overlay").onclick=closeModals;
}
function resetFilters(){state.selected=new Set(state.stores.map(s=>s.id));$("#location-select").value="todas";$("#discount-only").checked=false;$("#hide-accessories").checked=true;$("#include-refurbished").checked=true;renderStores()}
function runIfQuery(){if($("#search-input").value.trim().length>1)search()}
function show(name){["welcome-state","loading-state","empty-state","results"].forEach(id=>$("#"+id).classList.toggle("hidden",id!==name))}
async function search(){
  const query=$("#search-input").value.trim();if(query.length<2)return;
  if(state.controller)state.controller.abort();state.controller=new AbortController();show("loading-state");$("#filters").classList.remove("open");
  const p=new URLSearchParams({q:query,sort:$("#sort-select").value,location:$("#location-select").value,hide_accessories:$("#hide-accessories").checked,include_refurbished:$("#include-refurbished").checked,only_discounts:$("#discount-only").checked});
  if(state.selected.size&&state.selected.size<state.stores.length)p.set("stores",[...state.selected].join(","));
  history.replaceState(null,"",`?q=${encodeURIComponent(query)}`);
  try{const r=await fetch(`/api/search?${p}`,{signal:state.controller.signal});if(!r.ok)throw new Error(`HTTP ${r.status}`);const data=await r.json();state.results=data.results||[];state.stats=data.stats||{};state.breakdown=data.stores||{};if(!state.results.length){$("#empty-title").textContent="No encontramos coincidencias";$("#empty-copy").textContent="Prueba con el modelo exacto o activa más tiendas.";show("empty-state")}else{renderResults();show("results");$("#workspace").scrollIntoView({behavior:"smooth",block:"start"})}}
  catch(e){if(e.name==="AbortError")return;$("#empty-title").textContent="No pudimos completar la búsqueda";$("#empty-copy").textContent="Revisa tu conexión e inténtalo nuevamente en unos segundos.";show("empty-state")}
}
function renderResults(){
  const q=$("#search-input").value.trim();$("#results-total").textContent=state.results.length;$("#results-query").textContent=q;
  const best=state.stats.cheapest_item||[...state.results].sort((a,b)=>a.price-b.price)[0];const saving=Math.max(0,(state.stats.average_price||0)-best.price);
  $("#best-deal").innerHTML=`<div class="best-image">${imageTag(best)}</div><div class="best-copy"><span class="badge">Mejor precio encontrado</span><span class="store-name">en ${esc(best.store)}</span><h3>${esc(best.title)}</h3><p>${saving?`Ahorras ${money(saving)} frente al promedio`:"El precio más bajo de esta comparación"}</p></div><div class="best-price"><strong>${money(best.price)}</strong>${best.original_price?`<s>${money(best.original_price)}</s>`:""}<a href="${esc(safeUrl(best.url))}" target="_blank" rel="noopener noreferrer">Ver oferta <svg><use href="#external"></use></svg></a></div>`;
  $("#summary").innerHTML=`<div><span>Precio más bajo</span><b>${money(state.stats.lowest_price)}</b></div><div><span>Precio promedio</span><b>${money(state.stats.average_price)}</b></div><div><span>Precio más alto</span><b>${money(state.stats.highest_price)}</b></div><div><span>Ahorro posible</span><b>${money((state.stats.highest_price||0)-(state.stats.lowest_price||0))}</b></div>`;
  $("#store-summary").innerHTML=Object.values(state.breakdown).filter(s=>s.count).map(s=>`<span class="store-chip"><b>${esc(s.name)}</b> · ${s.count} desde ${money(s.lowest_price)}</span>`).join("");
  $("#product-grid").innerHTML=state.results.map(card).join("");
  $$(".heart").forEach(b=>b.onclick=()=>toggleFavorite(Number(b.dataset.index)));$$(".compare-add").forEach(b=>b.onclick=()=>toggleCompare(Number(b.dataset.index)));
}
function card(p,i){const fav=isFavorite(p),comp=state.compare.some(x=>productKey(x)===productKey(p));return `<article class="product-card"><div class="card-top"><span class="rank">#${i+1} · ${i===0?"Más barato":"Oferta"}</span><span class="condition">${esc(p.condition||"Nuevo")}</span><button class="heart ${fav?"active":""}" data-index="${i}" aria-label="Guardar"><svg><use href="#heart"></use></svg></button></div><a class="card-image" href="${esc(safeUrl(p.url))}" target="_blank" rel="noopener noreferrer">${imageTag(p)}</a><div class="card-store"><i class="store-dot" style="background:${esc(p.store_color)}"></i>${esc(p.store)}</div><h3 class="card-title">${esc(p.title)}</h3><div class="card-meta">${p.pickup_available?"<span>Retiro disponible</span>":""}${p.card_name?`<span class="card-only">${esc(p.card_name)}</span>`:""}</div><div class="price-line"><div><strong>${money(p.price)}</strong>${p.original_price?`<s>${money(p.original_price)}</s>`:""}</div>${p.discount_percent?`<span class="discount">-${Number(p.discount_percent)}%</span>`:""}</div><div class="card-actions"><a href="${esc(safeUrl(p.url))}" target="_blank" rel="noopener noreferrer">Ver en ${esc(p.store)}</a><button class="compare-add ${comp?"active":""}" data-index="${i}" title="Comparar"><svg><use href="#scale"></use></svg></button></div></article>`}
function toggleFavorite(i){const p=state.results[i],key=productKey(p),at=state.favorites.findIndex(x=>productKey(x)===key);at>=0?state.favorites.splice(at,1):state.favorites.push(p);save();renderResults()}
function updateFavoriteCount(){$("#favorites-count").textContent=state.favorites.length}
function renderFavorites(){const box=$("#favorites-list");box.innerHTML=state.favorites.length?state.favorites.map((p,i)=>`<div class="favorite-item">${imageTag(p)}<div><h3>${esc(p.title)}</h3><p>${money(p.price)} · ${esc(p.store)}</p><a href="${esc(safeUrl(p.url))}" target="_blank" rel="noopener">Ver oferta</a></div><button data-remove="${i}">×</button></div>`).join(""):'<p class="muted">Aún no guardaste productos.</p>';$$('[data-remove]').forEach(b=>b.onclick=()=>{state.favorites.splice(Number(b.dataset.remove),1);save();renderFavorites();renderResults()})}
function toggleCompare(i){const p=state.results[i],key=productKey(p),at=state.compare.findIndex(x=>productKey(x)===key);if(at>=0)state.compare.splice(at,1);else if(state.compare.length<3)state.compare.push(p);updateCompare();renderResults()}
function updateCompare(){$("#compare-bar").classList.toggle("hidden",!state.compare.length);$("#compare-count").textContent=state.compare.length;$("#compare-thumbs").innerHTML=state.compare.map(p=>imageTag(p,"compare-thumb")).join("")}
function openModal(type){const modal=$(type==="favorites"?"#favorites-modal":"#compare-modal");if(type==="favorites")renderFavorites();else renderCompare();$("#modal-overlay").classList.remove("hidden");modal.showModal()}
function closeModals(){$$("dialog[open]").forEach(d=>d.close());$("#modal-overlay").classList.add("hidden")}
function renderCompare(){const ps=state.compare;if(!ps.length){$("#compare-content").innerHTML='<p class="muted">Selecciona productos desde los resultados.</p>';return}const row=(label,fn)=>`<tr><th>${label}</th>${ps.map(p=>`<td>${fn(p)}</td>`).join("")}</tr>`;$("#compare-content").innerHTML=`<table class="compare-table">${row("Producto",p=>imageTag(p)+`<br>${esc(p.title)}`)}${row("Precio",p=>`<b>${money(p.price)}</b>`)}${row("Tienda",p=>esc(p.store))}${row("Estado",p=>esc(p.condition))}${row("Pago",p=>esc(p.payment_method))}${row("Comprar",p=>`<a href="${esc(safeUrl(p.url))}" target="_blank" rel="noopener">Ver oferta</a>`)}</table>`}
function exportCsv(){if(!state.results.length)return;const quote=v=>`"${String(v??"").replaceAll('"','""')}"`;const rows=[["Posición","Tienda","Producto","Precio PEN","Condición","URL"],...state.results.map((p,i)=>[i+1,p.store,p.title,p.price,p.condition,p.url])];const blob=new Blob(["\ufeff"+rows.map(r=>r.map(quote).join(",")).join("\n")],{type:"text/csv;charset=utf-8"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download=`comparacion-${$("#search-input").value.trim().replace(/\s+/g,"-").toLowerCase()}.csv`;a.click();URL.revokeObjectURL(a.href)}
