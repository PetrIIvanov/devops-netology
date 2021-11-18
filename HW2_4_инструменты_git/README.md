<h2>Домашнее задание к занятию «2.4. Инструменты Git - Петр Иванов</h2>

<h3>1. Найдите полный хеш и комментарий коммита, хеш которого начинается на aefea.v</h3>
<b>$ git show aefea</b>  

commit aefead2207ef7e2aa5dc81a34aedf0cad4c32545  

Author: Alisdair McDiarmid <alisdair@users.noreply.github.com><br>
Date:   Thu Jun 18 10:29:58 2020 -0400  

    Update CHANGELOG.md  

diff --git a/CHANGELOG.md b/CHANGELOG.md
index 86d70e3e0..588d807b1 100644

<h3>2. Какому тегу соответствует коммит 85024d3?</h3>
<b>$ git log 85024d3 -2 --oneline</b>  
v0.12.23

<h3>Сколько родителей у коммита b8d720? Напишите их хеши.</h3>  
<b>$ git log b8d720 -3 --all --oneline</b>  

<b>$ git log b8d720 -3 --all --oneline --reverse</b>  

такое впечатление что коммит b8d720 слили с f14166a5b (origin/nf/nov21-migrate-away-from-cloud), у последнего только один предок 
  


<h3>Перечислите хеши и комментарии всех коммитов которые были сделаны между тегами v0.12.23 и v0.12.24.</h3>
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


<h3>Найдите коммит в котором была создана функция func providerSource, ее определение в коде выглядит так func providerSource(...) (вместо троеточего перечислены аргументы).</h3>
<b>$ git log -G "func providerSource(\s)*[(]" --source --all --oneline</b>
Находит коммиты  

	cb8bb69ee       refs/remotes/origin/revamp-cli-config (origin/revamp-cli-config) cliconfig: Move HCL 1.0-based language out of the way
	5af1e6234       refs/remotes/origin/alisdair/getproviders-retries-bad-branch-do-not-use main: Honor explicit provider_installation CLI config when present
	8c928e835       refs/remotes/origin/alisdair/getproviders-retries-bad-branch-do-not-use main: Consult local directories as potential mirrors of providers
  
далее делаем чекаут 8c928e835
<b>$ git grep -p -n --break --heading "func providerSource"</b>
Находит 
	provider_source.go
	3=import (
	19:func providerSource(services *disco.Disco) getproviders.Source {
  
Наверное оно не пошло в main, смущает коммент к коммиту. Или это потом было добавлено, что функция выпиливается из модуля. Короче надо смотреть что там. 

<h3>Найдите все коммиты в которых была изменена функция globalPluginDirs.</h3>
<b>$ git grep -p -n --break --heading "globalPluginDirs"</b> 
Находит файл источник - plugins.go

Далеее
<b>$ git log -L :'globalPluginDirs':plugins.go --pretty=oneline -q</b>
показывает нам коммиты

	78b12205587fe839f10d946ea3fdc06719decb05 Remove config.go and update things using its aliases
	52dbf94834cb970b510f2fba853a5b49ad9b1a46 keep .terraform.d/plugins for discovery
	41ab0aef7a0fe030e84018973a64135b11abcd70 Add missing OS_ARCH dir to global plugin paths
	66ebff90cdfaa6938f26f908c7ebad8d547fea17 move some more plugin search path logic to command
	8364383c359a6b738a436d1b7745ccdce178df47 Push plugin discovery down into command package
   
<h3>Кто автор функции synchronizedWriters?</h3>
Нет такой функции ни в main, ни в истории, есть FieldWriters. 

