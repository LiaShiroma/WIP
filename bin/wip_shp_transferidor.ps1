#####################################################################################################################################
# 26/11/2019 Versão 1.0	- Projeto WIP																								#
# Download arquivos fontes do Sharepoint para máquina física																		#
#																																	#
# Módulo PnPOnline do PowerShell é necessário																						#
# Veja mais em: https://docs.microsoft.com/pt-br/powershell/sharepoint/sharepoint-pnp/sharepoint-pnp-cmdlets?view=sharepoint-ps		#
#																																	#
#####################################################################################################################################

$date = Get-Date -Format "yyyyMMdd"

#Read Conf File
cat /PROD/conf/init.conf | ForEach-Object -Begin {$conf=@{}} -Process {

	 $k = [regex]::split($_,'='); 
	 
	 if(($k[0].CompareTo("") -ne 0) -and ($k[0].StartsWith("[") -ne $True)){ 
		$conf.Add($k[0], $k[1]) 
	 } 
	 
 }

#Connection
$siteUrl = $conf['SITE_URL']

#Download File Location
$downloadLocation = $conf['DIR'] + $date

If(!(test-path $downloadLocation ))
{
	New-Item -Path $conf['DIR'] -Name $date -ItemType "directory"
}

#MFA Login
Connect-PnPOnline -Url $siteUrl -UseWebLogin -CreateDrive
$ctx = Get-PnPContext
$list = Get-PnPList $conf['PNP_LIST']

#Get Root Files
$files = $list.RootFolder.Files

$ctx.Load($files)
$ctx.ExecuteQuery()

#Downloading
foreach ($file in $files)
{
	echo $file.ServerRelativeUrl
	Get-PNPFile -Force -ServerRelativeUrl $file.ServerRelativeUrl -Path $DownloadLocation -Filename $file.Name -AsFile
	#Remove-PnPFile -SiteRelativeUrl $file.ServerRelativeUrl -Recycle #Sem permissão para deleção
}