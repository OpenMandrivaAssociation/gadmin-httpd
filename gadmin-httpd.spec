Summary:	Easy to use GTK+ frontend for the Apache httpd webserver
Name:		gadmin-httpd
Version:	0.1.2
Release:	%mkrel 1
License:	GPLv2+
Group:		System/Configuration/Networking
URL:		http://www.gadmintools.org/
Source0:	http://mange.dynalias.org/linux/%{name}/%{name}-%{version}.tar.gz
Source1:	%{name}.pam
BuildRequires:	gtk+2-devel
BuildRequires:	ImageMagick
BuildRequires:  desktop-file-utils
Requires:	apache	
Requires:	usermode-consoleonly
Obsoletes:	gadminhttpd
Provides:	gadminhttpd
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
GAdminHTTPD is an easy to use GTK+ frontend for the Apache httpd webserver.

%prep

%setup -q

%build

%configure2_5x

%make

%install
rm -rf %{buildroot}

%makeinstall INSTALL_USER=`id -un` INSTALL_GROUP=`id -gn`

# pam auth
install -d %{buildroot}%{_sysconfdir}/pam.d/
install -d %{buildroot}%{_sysconfdir}/security/console.apps

install -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/pam.d/%{name}
install -m 644 etc/security/console.apps/%{name} %{buildroot}%{_sysconfdir}/security/console.apps/%{name}

# locales
%find_lang %name

# Mandriva Icons
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_miconsdir}
install -d %{buildroot}%{_liconsdir}
convert -geometry 48x48 pixmaps/%{name}.png %{buildroot}%{_liconsdir}/%{name}.png
convert -geometry 32x32 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/%{name}.png
convert -geometry 16x16 pixmaps/%{name}.png %{buildroot}%{_miconsdir}/%{name}.png

# Menu
mkdir -p %{buildroot}%{_datadir}/applications
mv desktop/%{name}.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
perl -pi -e 's,%{name}.png,%{name},g' %{buildroot}%{_datadir}/applications/*
desktop-file-install --vendor="" \
    --remove-category="Application" \
    --add-category="Settings;Network;GTK;" \
    --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

# Prepare usermode entry
mv %{buildroot}%{_sbindir}/%{name} %{buildroot}%{_sbindir}/%{name}.real
ln -s %{_bindir}/consolehelper %{buildroot}%{_sbindir}/%{name}

mkdir -p %{buildroot}%{_sysconfdir}/security/console.apps
cat > %{buildroot}%{_sysconfdir}/security/console.apps/%{name} <<_EOF_
USER=root
PROGRAM=%{_sbindir}/%{name}.real
SESSION=true
FALLBACK=false
_EOF_

rm -rf %{buildroot}%{_datadir}/doc/%{name}

%if %mdkversion < 200900
%post
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING AUTHORS ChangeLog
%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}
%{_sbindir}/%{name}
%{_sbindir}/%{name}.real
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/*.png
%{_datadir}/pixmaps/%{name}/*.png
%{_datadir}/pixmaps/%{name}/%{name}.png
%{_iconsdir}/%{name}.png
%{_miconsdir}/%{name}.png
%{_liconsdir}/%{name}.png
