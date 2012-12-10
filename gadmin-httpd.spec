# if I fix the string literal errors according to the wiki Problems
# page, it crashes on startup - AdamW 2009/01
%define Werror_cflags %nil

Summary:	Easy to use GTK+ frontend for the Apache HTTPD webserver
Name:		gadmin-httpd
Version:	0.1.4
Release:	2
License:	GPLv3+
Group:		System/Configuration/Networking
URL:		http://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
BuildRequires:	gtk+2-devel
BuildRequires:	imagemagick
BuildRequires:  desktop-file-utils
Requires:	apache	
Requires:	usermode-consoleonly
Obsoletes:	gadminhttpd
Provides:	gadminhttpd

%description
GAdmin-HTTPD is an easy to use GTK+ frontend for the Apache httpd webserver.

%prep
%setup -q

%build
%configure2_5x
%make

%install
%makeinstall_std
#INSTALL_USER=`id -un` INSTALL_GROUP=`id -gn`

# pam auth
install -d %{buildroot}%{_sysconfdir}/pam.d/
install -d %{buildroot}%{_sysconfdir}/security/console.apps

install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 644 etc/security/console.apps/%{name} %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

# Icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
convert -geometry 48x48 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -geometry 32x32 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -geometry 16x16 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png

# Menu
mkdir -p %{buildroot}%{_datadir}/applications
sed -i -e 's,%{name}.png,%{name},g' desktop/%{name}.desktop
sed -i -e 's,GADMIN-HTTPD,Gadmin-HTTPD,g' desktop/%{name}.desktop
mv desktop/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install --vendor="" \
    --remove-category="Application" \
    --add-category="Settings;Network;GTK;" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# Prepare usermode entry
mkdir -p %{buildroot}%{_bindir}
mv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/%{name}.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<_EOF_
USER=root
PROGRAM=%{_sbindir}/%{name}.real
SESSION=true
FALLBACK=false
_EOF_

rm -rf %{buildroot}%{_datadir}/doc/%{name}

%files
%defattr(-,root,root,0755)
%doc COPYING AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%{_bindir}/%{name}
%{_sbindir}/%{name}.real
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/%{name}/*.png
%{_iconsdir}/hicolor/*/apps/%{name}.png



%changelog
* Sat Aug 14 2010 Funda Wang <fwang@mandriva.org> 0.1.4-1mdv2011.0
+ Revision: 569754
- new version 0.1.4

* Sun Feb 28 2010 Funda Wang <fwang@mandriva.org> 0.1.2-3mdv2010.1
+ Revision: 512756
- fix build

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sun Jan 04 2009 Adam Williamson <awilliamson@mandriva.org> 0.1.2-2mdv2009.1
+ Revision: 324163
- install consolehelper link to /usr/bin not /usr/sbin, so it works right
- don't use ALL CAPS in menu entry
- fd.o icons
- clean description a bit
- new license policy
- disable Werror (if I try and fix it, it crashes on startup)

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Sep 09 2008 Emmanuel Andry <eandry@mandriva.org> 0.1.2-1mdv2009.0
+ Revision: 283230
- import gadmin-httpd


