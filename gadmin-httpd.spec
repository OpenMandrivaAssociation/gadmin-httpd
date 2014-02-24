# if I fix the string literal errors according to the wiki Problems
# page, it crashes on startup - AdamW 2009/01
%define Werror_cflags %nil

Summary:	Easy to use GTK+ frontend for the Apache HTTPD webserver
Name:		gadmin-httpd
Version:	0.1.4
Release:	3
License:	GPLv3+
Group:		System/Configuration/Networking
Url:		http://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
BuildRequires:	desktop-file-utils
BuildRequires:	imagemagick
BuildRequires:	pkgconfig(gtk+-2.0)
Requires:	apache-base
Requires:	usermode-consoleonly

%description
GAdmin-HTTPD is an easy to use GTK+ frontend for the Apache httpd webserver.

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

#----------------------------------------------------------------------------

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

