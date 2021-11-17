<h2>Домашнее задание к занятию «2.4. Инструменты Git - Петр Иванов</h2>

<h3>1. Найдите полный хеш и комментарий коммита, хеш которого начинается на aefea.v</h3>
<b>$ git show aefea</b>  

commit aefead2207ef7e2aa5dc81a34aedf0cad4c32545  

Author: Alisdair McDiarmid <alisdair@users.noreply.github.com><br>
Date:   Thu Jun 18 10:29:58 2020 -0400  

    Update CHANGELOG.md  

diff --git a/CHANGELOG.md b/CHANGELOG.md
index 86d70e3e0..588d807b1 100644

<h3>2. Какому тегу соответствует коммит 85024d3?</h>
<b>$ git log 85024d3 -2 --oneline</b>  
v0.12.23

<h4>Сколько родителей у коммита b8d720? Напишите их хеши.</h4>  
<b>$ git log b8d720 -3 --all --oneline</b>  

<b>$ git log b8d720 -3 --all --oneline --reverse</b>  

такое впечатление что коммит b8d720 слили с f14166a5b (origin/nf/nov21-migrate-away-from-cloud), у последнего только один предок 
  


<h3>Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24.</h4>
<b>$ git log v0.12.23..v0.12.24 --oneline</b>  

	33ff1c03b (tag: v0.12.24) v0.12.24
	b14b74c49 [Website] vmc provider links
	3f235065b Update CHANGELOG.md
	6ae64e247 registry: Fix panic when server is unreachable
	5c619ca1b website: Remove links to the getting started guide's old location
	06275647e Update CHANGELOG.md
	d5f9411f5 command: Fix bug when using terraform login on Windows
	4b6d06cc5 Update CHANGELOG.md
	dd01a3507 Update CHANGELOG.md
	225466bc3 Cleanup after v0.12.23 release


<h4>Найдите коммит в котором была создана функция func providerSource, ее определение в коде выглядит так func providerSource(...) (вместо троеточего перечислены аргументы).</h4>
<h4>Найдите все коммиты в которых была изменена функция globalPluginDirs.</h4>
<h4>Кто автор функции synchronizedWriters?</h4>
