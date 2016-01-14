%{?scl:%scl_package devassistant}
%{!?scl:%global pkg_name %{name}}

%global shortname da

#%%global prerel b1

Name:           %{?scl_prefix}devassistant
Version:        0.9.3
Release:        %{?prerel:0.}3%{?prerel:.%{prerel}}%{?dist}
Summary:        DevAssistant - Making life easier for developers

License:        GPLv2+ and CC-BY-SA
URL:            https://github.com/bkabrda/devassistant
Source0:        https://pypi.python.org/packages/source/d/%{pkg_name}/%{pkg_name}-%{version}%{?prerel}.tar.gz
Patch0:         %{pkg_name}-0.9.0-alter-paths-downstream.patch
Patch2:         %{pkg_name}-0.9.0-dont-require-pygithub.patch
Patch3:         %{pkg_name}-0.9.0-fix-old-six.patch
Patch4:         %{pkg_name}-0.9.0-fix-directory-not-writable.patch
BuildArch:      noarch
 
BuildRequires:  python-devel
BuildRequires:  python-setuptools
BuildRequires:  python-sphinx

Requires:       git
Requires:       gtk3
Requires:       polkit
Requires:       pygobject3
Requires:       python-argparse
Requires:       python-setuptools
Requires:       python-jinja2
Requires:       %{?scl_prefix}python-progress
Requires:       python-six
Requires:       PyYAML
Requires:       yum
%{?scl:Requires: %{scl}-runtime}
%{?scl:BuildRequires: %{scl}-runtime}

%description
DevAssistant can help you with creating and setting up basic projects
in various languages, installing dependencies, setting up environments,
working with source control, etc.

%package doc
Summary:       Documentation for %{pkg_name}
Group:         Documentation
Requires:      %{name} = %{version}-%{release}

%description doc
Package with user and developer documentation of %{pkg_name}.

%prep
%setup -q -n %{pkg_name}-%{version}%{?prerel}
# Remove bundled egg-info
rm -rf %{pkg_name}.egg-info
# remove Fedora assistant set
rm -rf %{pkg_name}/data

# don't require PyGithub in DTS version
%patch2 -p0

# fix usage of six.PY2 for old six versions
%patch3 -p1

# fix raising an exception when directory is not writable
%patch4 -p1

%build
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py build
%{?scl:EOF}

pushd docs
make html
rm _build/html/.buildinfo
popd

%install
%{?scl:scl enable %{scl} - << \EOF}
%{__python} setup.py install --skip-build --root %{buildroot} \
    --install-purelib %{python_sitelib} \
    --install-scripts %{_bindir}
%{?scl:EOF}

# install manpages for both short and long forms of the binaries
mkdir -p %{buildroot}%{_mandir}/man1
install -p manpages/%{shortname}.1 %{buildroot}%{_mandir}/man1
install -p manpages/%{shortname}-gui.1 %{buildroot}%{_mandir}/man1
install -p manpages/%{pkg_name}.1 %{buildroot}%{_mandir}/man1
install -p manpages/%{pkg_name}-gui.1 %{buildroot}%{_mandir}/man1/%{pkg_name}-gui.1

# create the %%{_datadir} hierarchy
pushd %{buildroot}%{_datadir}
mkdir -p %{pkg_name}/{assistants,files,icons,snippets}
mkdir -p %{pkg_name}/assistants/{crt,mod,prep,task}
# files are also for snippets
mkdir -p %{pkg_name}/files/{crt,mod,prep,task,snippets}
mkdir -p %{pkg_name}/icons/{crt,mod,prep,task}

# first, do the alterations to paths in devassistant
pushd %{buildroot}%{python_sitelib}
patch -p0 < %{PATCH0}
sed -i 's|_DATADIR_DEVASSISTANT|%{_datadir}/%{pkg_name}|' devassistant/settings.py
sed -i 's|_DATADIR_LOCAL_DEVASSISTANT|%{_prefix}/local/share/%{pkg_name}|' devassistant/settings.py
popd

%files
%doc README.rst LICENSE
%{_bindir}/%{shortname}
%{_bindir}/%{shortname}-gui
%{_bindir}/%{pkg_name}
%{_bindir}/%{pkg_name}-gui
%{_datadir}/%{pkg_name}
%{_mandir}/man1/%{shortname}.1.gz
%{_mandir}/man1/%{shortname}-gui.1.gz
%{_mandir}/man1/%{pkg_name}.1.gz
%{_mandir}/man1/%{pkg_name}-gui.1.gz
%{python_sitelib}/%{pkg_name}
%{python_sitelib}/%{pkg_name}-%{version}%{?prerel}-py?.?.egg-info

%files doc
%doc docs/_build/html

%changelog
* Wed Feb 18 2015 Tomas Radej <tradej@redhat.com> - 0.9.3-3
- Fix usage of six.PY2 for older six versions
Resolves: rhbz#1193936

* Tue Jan 20 2015 Slavek Kabrda <bkabrda@redhat.com> - 0.9.3-2
- Make patch 0 (alter paths downstream) apply cleanly.

* Thu Jan 08 2015 Slavek Kabrda <bkabrda@redhat.com> - 0.9.3-1
- Update to 0.9.3 final
Resolves: rhbz#1167913

* Mon Jun 23 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.1-1
- Update to 0.9.1 final

* Thu May 29 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.0-3
- Make paths alteration patch apply cleanly.

* Tue May 27 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.0-2
- Remove the unsupported code from GUI.

* Tue May 27 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.0-1
- Update to 0.9.0 final

* Thu May 22 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.0-0.3.b1
- Rebuilt for RHEL 7

* Thu May 22 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.0-0.2.b1
- Alter /usr/local/share/devassistant path to point to /opt, too.

* Wed May 21 2014 Bohuslav Kabrda <bkabrda@redhat.com> - 0.9.0-0.1.b1
- Rebuilt for devassist09
- Updated to DevAssistant 0.9.0b1

* Mon Apr 14 2014 Tomas Radej <tradej@redhat.com> - 0.8.0-3
- Added CC-BY-SA to License field because of appdata.xml

* Fri Feb 28 2014 Miro Hrončok <mhroncok@redhat.com> - 0.8.0-2
- Backport fix of GitHub errors.

* Wed Dec 04 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.8.0-1
- Update to 0.8.0.
- Don't create the /usr/local hierarchy, leave it up to users.

* Wed Oct 02 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.7.0-1
- Update to 0.7.0.

* Wed Aug 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.1-2
- Properly create and own the /usr/local hierarchy.

* Wed Aug 28 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.6.1-1
- Update to 0.6.1.
- Introduce gui, add its dependencies.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jul 26 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.5.0-1
- Update to 0.5.0.
- Regenerated patch0.

* Wed Jul 17 2013 Petr Pisar <ppisar@redhat.com> - 0.4.0-3
- Perl 5.18 rebuild

* Wed Jul 03 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.0-2
- Fix manpage typo, rhbz#980646.

* Mon Jul 01 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.4.0-1
- Update to 0.4.0.

* Wed May 15 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.3.1-1
- Update to 0.3.1.
- Remove no longer needed dependencies (jinja2, plumbum).

* Wed Mar 20 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.2-1
- Update to 0.2.2 because of minor bug in 0.2.1.

* Wed Mar 20 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.1-1
- Update to devassistant 0.2.1.
- Introduce bash completion script.

* Mon Mar 18 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.2.0-1
- Update to devassistant 0.2.0.
- Move assistants and snippets to %%{datadir}/%%{pkg_name}.
- Introduce manpage.

* Tue Mar 12 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.1.0-3
- Move templates to %%{_datadir}.

* Tue Mar 12 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.1.0-2
- Use BR: python2-devel instead of python-devel.

* Fri Mar 08 2013 Bohuslav Kabrda <bkabrda@redhat.com> - 0.1.0-1
- Initial package.
