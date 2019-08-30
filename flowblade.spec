%global commit0 9aee5f25f35bcaf3f9eb28c8bfc64061734358ba
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

Name:           flowblade
Version:        2.2
Release:	7%{?gver}%{?dist}
License:        GPLv3
Summary:        Multitrack non-linear video editor for Linux
Url:            https://github.com/jliljebl/flowblade
Source0:	https://github.com/jliljebl/flowblade/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Patch0:       	wblade-001_sys_path.patch

BuildRequires:  desktop-file-utils
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:	gettext
Requires:       ffmpeg
Requires:       mlt-python
Requires:       frei0r-plugins >= 1.4
Requires:       gmic
Requires:       gtk3
Requires:       ladspa-swh-plugins
Requires:       ladspa-calf-plugins
Requires:       librsvg2
Requires:       python-dbus
Requires:       python-gobject
%if 0%{?fedora} >= 24
Requires:       python2-numpy
Requires:       python2-pillow
%else
Requires:       numpy
Requires:       python-pillow
%endif
%if 0%{?fedora} >= 25
Requires:       mlt-freeworld
%endif

BuildArch:      noarch

%description
Flowblade Movie Editor is a multitrack non-linear video editor for Linux
released under GPL 3 license.

Flowblade is designed to provide a fast, precise and robust editing 
experience.

In Flowblade clips are usually automatically placed tightly after or 
between clips when they are inserted on the timeline. Edits are fine 
tuned by trimming in and out points of clips, or by cutting and deleting 
parts of clips.

Flowblade provides powerful tools to mix and filter video and audio. 

%prep
%setup -n %{name}-%{commit0} 
%patch0 -p1
pushd flowblade-trunk
# patching flowblade, and avoid message 'small screen'
sed -i 's/1151/1024/g' Flowblade/app.py

# fix wrong-script-interpreter errors
sed -i -e 's@#!/usr/bin/env python@#!/usr/bin/python2@g' Flowblade/launch/*

# fix to %%{_datadir}/locale
sed -i "s|respaths.LOCALE_PATH|'%{_datadir}/locale'|g" Flowblade/translations.py
popd

%build 
pushd flowblade-trunk
%py2_build
popd

%install 
pushd flowblade-trunk
%py2_install 

# fix permissions
chmod +x %{buildroot}%{python2_sitelib}/Flowblade/launch/*

# setup of mime is already done, so for what we need this file ?
rm %{buildroot}/usr/lib/mime/packages/flowblade

# move .mo files to /usr/share/locale the right place
for i in $(ls -d %{buildroot}%{python2_sitelib}/Flowblade/locale/*/LC_MESSAGES/ | sed 's/\(^.*locale\/\)\(.*\)\(\/LC_MESSAGES\/$\)/\2/') ; do
    mkdir -p %{buildroot}%{_datadir}/locale/$i/LC_MESSAGES/
    mv %{buildroot}%{python2_sitelib}/Flowblade/locale/$i/LC_MESSAGES/%{name}.mo \
        %{buildroot}%{_datadir}/locale/$i/LC_MESSAGES/
done

# E: non-executable-script
chmod a+x %{buildroot}%{python2_sitelib}/Flowblade/tools/clapperless.py

install -d -m 0755 %{buildroot}%{python2_sitelib}/Flowblade/res/css
cp Flowblade/res/css/gtk-flowblade-dark.css %{buildroot}%{python2_sitelib}/Flowblade/res/css

popd

%find_lang %{name}

sed -i 's|/usr/bin/env python|/usr/bin/python2|g' %{buildroot}/%{python2_sitelib}/Flowblade/tools/clapperless.py
sed -i 's|/bin/bash|/usr/bin/bash|g' %{buildroot}/%{python2_sitelib}/Flowblade/launch/natron_render.sh
sed -i 's|/usr/bin/env bash|/usr/bin/bash|g' %{buildroot}/%{python2_sitelib}/Flowblade/launch/flowbladephantom
sed -i 's|/bin/bash|/usr/bin/bash|g' %{buildroot}/%{python2_sitelib}/Flowblade/launch/natron_clip_export_start.sh

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/io.github.jliljebl.Flowblade.desktop

%post
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
  /usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :

%posttrans
/usr/bin/update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :


%files -f %{name}.lang
%doc flowblade-trunk/README
%license flowblade-trunk/COPYING
%{_bindir}/flowblade
%{_datadir}/applications/io.github.jliljebl.Flowblade.desktop
%{_mandir}/man1/flowblade.1.*
%{_datadir}/mime/
%{_datadir}/appdata/io.github.jliljebl.Flowblade.appdata.xml
%{_datadir}/icons/hicolor/128x128/apps/io.github.jliljebl.Flowblade.png
%{python2_sitelib}/Flowblade/
%{python2_sitelib}/flowblade*.egg-info


%changelog

* Thu Aug 29 2019 David Vasquez <davidva AT tutanota DOT com> - 2.2-7.git9aee5f2
- Updated to 2.2

* Mon Feb 04 2019 David Vasquez <davidva AT tutanota DOT com> - 2.0-7.gitaa923b5
- Updated to 2.0

* Wed Jul 11 2018 David Vasquez <davidva AT tutanota DOT com> - 1.16-4.git4c25c3c
- Updated to Current commit
- Fix crash by banning Qt producers to keep using Gtk producers after Qimage

* Sat Jun 30 2018 David Vasquez <davidva AT tutanota DOT com> - 1.16-3.git3fdb76d
- Updated to 1.16-3.git3fdb76d

* Sun Apr 01 2018 David Vasquez <davidva AT tutanota DOT com> - 1.16-2.gitdd4e190
- Updated to 1.16-2.gitdd4e190

* Fri Jan 19 2018 David Vasquez <davidva AT tutanota DOT com> - 1.14-4.gitccda303
- Updated to 1.14-4.gitccda303

* Wed Nov 08 2017 David Vasquez <davidjeremias82 AT gmail DOT com> - 1.14-3.gitcad77b5
- Updated to 1.14-3.gitcad77b5

* Fri Oct 06 2017 David Vasquez <davidjeremias82 AT gmail DOT com> - 1.14-2.gitb2b5f57
- Updated to 1.14-2.gitb2b5f57

* Sat Mar 25 2017 David Vasquez <davidjeremias82 AT gmail DOT com> - 1.12.2-2.gite156175
- Updated to 1.12.2-2-20170325gite156175

* Fri Mar 24 2017 Martin Gansser <martinkg@fedoraproject.org> - 1.12.0-1.gitfd577a9
- Update to 1.12.0-1.gitfd577a9

* Fri Mar 24 2017 Martin Gansser <martinkg@fedoraproject.org> - 1.12.0-1.gitfd577a9
- Update to 1.12.0-1.gitfd577a9

* Sun Mar 19 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.10.0-4.git9365491
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Dec 22 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.10.0-3.git25c07ce
- rebuild

* Fri Dec 16 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.10.0-2.git25c07ce
- Readd ffmpeg
- Add Requires mlt-freeworld in a if clause

* Thu Dec 15 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.10.0-1.git25c07ce
- Update to 1.10.0-1.git25c07ce
- Dropped Requires ffmpeg
- Add Requires mlt-freeworld

* Thu Sep 22 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.8.0-1.git9365491
- Update to 1.8.0-1.git9365491

* Fri Aug 26 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.6.0-5.gitc847b32
- Fix python requires for F23 (rfbz#4213)

* Wed Aug 17 2016 Leigh Scott <leigh123linux@googlemail.com> - 1.6.0-4.gitc847b32
- Update package requires for git snapshot

* Mon Aug 01 2016 Sérgio Basto <sergio@serjux.com> - 1.6.0-3.gitc847b32
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 30 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.6.0-2.gitc847b32
- Update to 1.6.0-2.gitc847b32

* Thu Jun 09 2016 Martin Gansser <martinkg@fedoraproject.org> - 1.6.0-1.git50f6fca
- Update to 1.6.0

* Mon Nov 30 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.4.0-1.git3f5d08d
- Update to 1.4.0

* Fri Sep 11 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.2.0-1.git7d98158
- Update to 1.2.0

* Thu Aug 27 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-6.git7d98158
- spec cleanup

* Sat Jul 18 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-5.git94f69ce
- dropped gnome-python2-gnomevfs requirement
- dropped ladspa requirement
- dropped pycairo requirement
- dropped mlt requirement
- dropped calf requirement
- dropped numpy requirement
- dropped cairo requirement

* Mon Jun 22 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-4.git94f69ce
- Fix file permissions before and after build
- Remove /usr/lib/mime/packages/flowblade file 
- move .mo files to /usr/share/locale

* Sun Jun 21 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-3.git94f69ce
- added flowblade.patch
- put setup.py into %%build section
- added macro %%find_lang
- fixed locale path 

* Sat Jun 20 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-2.git94f69ce
- used macro %%{python_sitearch}
- spec file cleanup
- mime file belong to %%{_libexecdir}

* Fri Jun 19 2015 Martin Gansser <martinkg@fedoraproject.org> - 1.1.0-1.git94f69ce
- Update to 1.1.0

* Fri Mar 20 2015 David Vasquez <davidjeremias82 AT gmail DOT com> - 0.18.0-1
- Updated to 0.18.0

* Sat Jul 05 2014 David Vasquez <davidjeremias82@ dat com> 0.12.0-1
- Updated to 0.12.0

* Thu Oct 24 2013 David Vasquez <davidjeremias82@ dat com> 0.10.0-1
- Initial build rpm Fedora

