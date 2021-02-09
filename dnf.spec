#
# spec file for package dnf
#
# Copyright (c) 2020 SUSE LLC
# Copyright (c) 2020-2021 Neal Gompa <ngompa13@gmail.com>.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%global hawkey_version 0.57.0
%global libcomps_version 0.1.8
%global libmodulemd_version 2.9.3
%global rpm_version 4.14.0
%global min_plugins_core 4.0.16
%global min_plugins_extras 4.0.4

%global confdir %{_sysconfdir}/%{name}

%global pluginconfpath %{confdir}/plugins

%global py3pluginpath %{python3_sitelib}/dnf-plugins

# YUM v3 has been removed from openSUSE Tumbleweed as of 20191119
%if 0%{?sle_version} && 0%{?sle_version} < 160000
%bcond_with as_yum
%else
%bcond_without as_yum
%endif

%if %{with as_yum}
%global yum_subpackage_name yum
%else
%global yum_subpackage_name dnf-yum
%endif

# Tests fail (possibly due to failures in libdnf tests on SUSE)
# Until those are resolved, these will remain disabled
%bcond_with tests

Name:           dnf
Version:        4.6.0
Release:        0
Summary:        Package manager forked from Yum, using libsolv as a dependency resolver
# For a breakdown of the licensing, see PACKAGE-LICENSING
License:        GPL-2.0-or-later AND GPL-2.0-only
Group:          System/Packages
URL:            https://github.com/rpm-software-management/dnf
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  bash-completion
BuildRequires:  cmake
BuildRequires:  gettext
BuildRequires:  python3-Sphinx
BuildRequires:  python3-bugzilla
BuildRequires:  systemd-rpm-macros
Requires:       python3-dnf = %{version}-%{release}
Recommends:     %{name}-lang >= %{version}
Recommends:     dnf-plugins-core
Recommends:     %{yum_subpackage_name}
Conflicts:      dnf-plugins-core < %{min_plugins_core}
Provides:       dnf-command(autoremove)
Provides:       dnf-command(check-update)
Provides:       dnf-command(clean)
Provides:       dnf-command(distro-sync)
Provides:       dnf-command(downgrade)
Provides:       dnf-command(group)
Provides:       dnf-command(history)
Provides:       dnf-command(info)
Provides:       dnf-command(install)
Provides:       dnf-command(list)
Provides:       dnf-command(makecache)
Provides:       dnf-command(mark)
Provides:       dnf-command(provides)
Provides:       dnf-command(reinstall)
Provides:       dnf-command(remove)
Provides:       dnf-command(repolist)
Provides:       dnf-command(repoquery)
Provides:       dnf-command(repository-packages)
Provides:       dnf-command(search)
Provides:       dnf-command(updateinfo)
Provides:       dnf-command(upgrade)
Provides:       dnf-command(upgrade-to)
BuildArch:      noarch
%{?systemd_ordering}

%description
DNF is a package manager for RPM systems that was forked from Yum. Among the
many improvements, it uses libsolv as a dependency resolver.

%package data
Summary:        Common data and configuration files for DNF
Group:          System/Packages
Obsoletes:      dnf-conf < 4.4.2
Provides:       dnf-conf = %{version}-%{release}
Recommends:     logrotate

%description data
This package provides the common data and configuration files for DNF.

%package -n %{yum_subpackage_name}
Summary:        As a Yum CLI compatibility layer, supplies %{_bindir}/yum redirecting to DNF
Group:          System/Packages
Requires:       dnf = %{version}-%{release}
%if %{with as_yum}
Obsoletes:      dnf-yum < %{version}-%{release}
Obsoletes:      yum < 4.0.0
Provides:       dnf-yum = %{version}-%{release}
# SUSE-specific split up of yum-utils features obsoleted by DNF itself...
%global yum_replaces() \
Obsoletes:      %{1} < 4.0.0 \
Provides:       %{1} = %{version}-%{release}

%yum_replaces  yum-aliases
%yum_replaces  yum-allowdowngrade
%yum_replaces  yum-basearchonly
%yum_replaces  yum-downloadonly
%yum_replaces  yum-fastestmirror
%yum_replaces  yum-priorities
%yum_replaces  yum-protect-packages
%yum_replaces  yum-protectbase
%yum_replaces  yum-refresh-updatesd
%yum_replaces  yum-tsflags

# yum-utils plugins with no replacement
Conflicts:      yum-filter-data
Conflicts:      yum-list-data
Conflicts:      yum-tmprepo
Conflicts:      yum-upgrade-helper
Conflicts:      yum-verify
%else
Conflicts:      yum
%endif

%description -n %{yum_subpackage_name}
As a Yum CLI compatibility layer, it supplies %{_bindir}/yum redirecting to DNF.

%package -n python3-dnf
Summary:        Python 3 interface to DNF
Group:          System/Packages
BuildRequires:  python3-curses
BuildRequires:  python3-devel
BuildRequires:  python3-gpg
BuildRequires:  python3-hawkey >= %{hawkey_version}
BuildRequires:  python3-libcomps >= %{libcomps_version}
BuildRequires:  python3-libmodulemd >= %{libmodulemd_version}
BuildRequires:  python3-nose
BuildRequires:  python3-rpm >= %{rpm_version}
Recommends:     (python3-dbus-python if NetworkManager)
Requires:       deltarpm
Requires:       dnf-data = %{version}-%{release}
Requires:       python3-curses
Requires:       python3-gpg
Requires:       python3-hawkey >= %{hawkey_version}
Requires:       python3-libcomps >= %{libcomps_version}
Requires:       python3-libmodulemd >= %{libmodulemd_version}
Requires:       python3-rpm >= %{rpm_version}
Recommends:     bash-completion
# DNF 2.0 doesn't work with old plugins
Conflicts:      python3-dnf-plugins-core < %{min_plugins_core}
Conflicts:      python3-dnf-plugins-extras-common < %{min_plugins_extras}
# Python 2 subpackage is no longer provided
Obsoletes:      python2-dnf < 4.0.10

%description -n python3-dnf
This package provides the Python 3 interface to DNF.

%lang_package

%package automatic
Summary:        Alternative CLI to "dnf upgrade" suitable for automatic, regular execution
Group:          System/Packages
BuildRequires:  systemd-rpm-macros
Requires:       dnf = %{version}-%{release}
%{?systemd_ordering}

%description automatic
Alternative CLI to "dnf upgrade" suitable for automatic, regular execution.

%prep
%autosetup -p1

# Fix sphinx-build run...
sed -e "s/sphinx-build-3/sphinx-build-%{python3_version}/" -i doc/CMakeLists.txt

%build
%cmake -DPYTHON_DESIRED:FILEPATH=%{__python3}
%make_build
make doc-man

%install
pushd ./build
%make_install
popd

%find_lang %{name}

mkdir -p %{buildroot}%{confdir}/repos.d
mkdir -p %{buildroot}%{confdir}/vars
mkdir -p %{buildroot}%{pluginconfpath}
mkdir -p %{buildroot}%{py3pluginpath}
mkdir -p %{buildroot}%{_sharedstatedir}/dnf
mkdir -p %{buildroot}%{_localstatedir}/log
mkdir -p %{buildroot}%{_var}/cache/dnf
touch %{buildroot}%{_localstatedir}/log/%{name}.log

ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-3 %{buildroot}%{_bindir}/dnf-automatic
ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/yum

%if %{with as_yum}
mkdir -p %{buildroot}%{_sysconfdir}/yum
ln -sr  %{buildroot}%{confdir}/%{name}.conf %{buildroot}%{_sysconfdir}/yum/yum.conf
ln -sr  %{buildroot}%{pluginconfpath} %{buildroot}%{_sysconfdir}/yum/pluginconf.d
ln -sr  %{buildroot}%{confdir}/protected.d %{buildroot}%{_sysconfdir}/yum/protected.d
ln -sr  %{buildroot}%{confdir}/repos.d %{buildroot}%{_sysconfdir}/yum/repos.d
ln -sr  %{buildroot}%{confdir}/vars %{buildroot}%{_sysconfdir}/yum/vars
%else
# We don't want this just yet...
rm -f %{buildroot}%{confdir}/protected.d/yum.conf
%endif

# This file is not used...
rm -f %{buildroot}%{confdir}/dnf-strict.conf

# We don't have ABRT/libreport in openSUSE
rm -rf %{buildroot}%{_sysconfdir}/libreport

%if %{with tests}
%check
pushd ./build
make ARGS="-V" test
popd
%endif

%files
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/dnf
%{_mandir}/man8/dnf.8*
%{_mandir}/man8/yum2dnf.8*
%{_mandir}/man7/dnf.modularity.7*
%{_mandir}/man5/dnf-transaction-json.5*
%dir %{_var}/cache/dnf
%{_unitdir}/dnf-makecache.service
%{_unitdir}/dnf-makecache.timer

%files lang -f %{name}.lang

%files data
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%dir %{confdir}
%dir %{pluginconfpath}
%dir %{confdir}/aliases.d
%dir %{confdir}/protected.d
%dir %{confdir}/repos.d
%dir %{confdir}/vars
%config(noreplace) %{confdir}/%{name}.conf
%config(noreplace) %{confdir}/aliases.d/zypper.conf
%config(noreplace) %{confdir}/protected.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%ghost %{_localstatedir}/log/hawkey.log
%ghost %{_localstatedir}/log/%{name}.log
%ghost %{_localstatedir}/log/%{name}.librepo.log
%ghost %{_localstatedir}/log/%{name}.rpm.log
%ghost %{_localstatedir}/log/%{name}.plugin.log
%dir %{_sharedstatedir}/%{name}
%ghost %{_sharedstatedir}/%{name}/groups.json
%ghost %{_sharedstatedir}/%{name}/yumdb
%ghost %{_sharedstatedir}/%{name}/history
%{_datadir}/bash-completion/completions/dnf
%{_mandir}/man5/dnf.conf.5.*
%{_tmpfilesdir}/dnf.conf

%files -n %{yum_subpackage_name}
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/yum
%{_mandir}/man8/yum.8.*
%{_mandir}/man8/yum-shell.8*
%{_mandir}/man5/yum.conf.5*
%{_mandir}/man1/yum-aliases.1*
%if %{with as_yum}
%dir %{_sysconfdir}/yum
%{_sysconfdir}/yum/yum.conf
%{_sysconfdir}/yum/pluginconf.d
%{_sysconfdir}/yum/protected.d
%{_sysconfdir}/yum/repos.d
%{_sysconfdir}/yum/vars
%config(noreplace) %{confdir}/protected.d/yum.conf
%endif

%files -n python3-dnf
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/dnf-3
%exclude %{python3_sitelib}/dnf/automatic
%{python3_sitelib}/dnf/
%dir %{py3pluginpath}

%files automatic
%license COPYING PACKAGE-LICENSING
%doc AUTHORS
%{_bindir}/%{name}-automatic
%config(noreplace) %{confdir}/automatic.conf
%{_mandir}/man8/%{name}-automatic.8.*
%{_unitdir}/%{name}-automatic.service
%{_unitdir}/%{name}-automatic.timer
%{_unitdir}/%{name}-automatic-notifyonly.service
%{_unitdir}/%{name}-automatic-notifyonly.timer
%{_unitdir}/%{name}-automatic-download.service
%{_unitdir}/%{name}-automatic-download.timer
%{_unitdir}/%{name}-automatic-install.service
%{_unitdir}/%{name}-automatic-install.timer
%{python3_sitelib}/%{name}/automatic

%post
%systemd_post %{name}-makecache.timer

%preun
%systemd_preun %{name}-makecache.timer

%postun
%systemd_postun_with_restart %{name}-makecache.timer

%post automatic
%systemd_post %{name}-automatic.timer %{name}-automatic-notifyonly.timer %{name}-automatic-download.timer %{name}-automatic-install.timer

%preun automatic
%systemd_preun %{name}-automatic.timer %{name}-automatic-notifyonly.timer %{name}-automatic-download.timer %{name}-automatic-install.timer

%postun automatic
%systemd_postun_with_restart %{name}-automatic.timer %{name}-automatic-notifyonly.timer %{name}-automatic-download.timer %{name}-automatic-install.timer

%if %{with as_yum}
%pretrans -n %{yum_subpackage_name} -p <lua>
-- Backup all legacy YUM package manager configuration subdirectories if they exist
yumconfpath = "%{_sysconfdir}/yum"
chkst = posix.stat(yumconfpath)
if chkst and chkst.type == "directory" then
  yumdirs = {"%{_sysconfdir}/yum/pluginconf.d", "%{_sysconfdir}/yum/protected.d", "%{_sysconfdir}/yum/repos.d", "%{_sysconfdir}/yum/vars"}
  for num,path in ipairs(yumdirs)
  do
    st = posix.stat(path)
    if st and st.type == "directory" then
      status = os.rename(path, path .. ".rpmmoved")
      if not status then
        suffix = 0
        while not status do
          suffix = suffix + 1
          status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
        end
        os.rename(path, path .. ".rpmmoved")
      end
    end
  end
end
%endif

%changelog


# Tests fail (possibly due to failures in libdnf tests on SUSE)
# Until those are resolved, these will remain disabled
%bcond_with tests

Name:           dnf
Version:        4.6.0
Release:        70.1
Summary:        Package manager forked from Yum, using libsolv as a dependency resolver
# For a breakdown of the licensing, see PACKAGE-LICENSING
License:        GPL-2.0-or-later AND GPL-2.0-only
Group:          System/Packages
URL:            https://github.com/rpm-software-management/dnf
Source0:        %{url}/archive/%{version}/%{name}-%{version}.tar.gz

BuildRequires:  bash-completion
BuildRequires:  cmake
BuildRequires:  gettext
BuildRequires:  python3-Sphinx
BuildRequires:  python3-bugzilla
BuildRequires:  systemd-rpm-macros
Requires:       python3-dnf = %{version}-%{release}
Recommends:     %{name}-lang
Recommends:     dnf-plugins-core
Recommends:     %{yum_subpackage_name}
Conflicts:      dnf-plugins-core < %{min_plugins_core}
Provides:       dnf-command(autoremove)
Provides:       dnf-command(check-update)
Provides:       dnf-command(clean)
Provides:       dnf-command(distro-sync)
Provides:       dnf-command(downgrade)
Provides:       dnf-command(group)
Provides:       dnf-command(history)
Provides:       dnf-command(info)
Provides:       dnf-command(install)
Provides:       dnf-command(list)
Provides:       dnf-command(makecache)
Provides:       dnf-command(mark)
Provides:       dnf-command(provides)
Provides:       dnf-command(reinstall)
Provides:       dnf-command(remove)
Provides:       dnf-command(repolist)
Provides:       dnf-command(repoquery)
Provides:       dnf-command(repository-packages)
Provides:       dnf-command(search)
Provides:       dnf-command(updateinfo)
Provides:       dnf-command(upgrade)
Provides:       dnf-command(upgrade-to)
BuildArch:      noarch
%{?systemd_ordering}

%description
DNF is a package manager for RPM systems that was forked from Yum. Among the
many improvements, it uses libsolv as a dependency resolver.

%package data
Summary:        Common data and configuration files for DNF
Group:          System/Packages
Obsoletes:      dnf-conf < 4.4.2
Provides:       dnf-conf = %{version}-%{release}
Recommends:     logrotate

%description data
This package provides the common data and configuration files for DNF.

%package -n %{yum_subpackage_name}
Summary:        As a Yum CLI compatibility layer, supplies %{_bindir}/yum redirecting to DNF
Group:          System/Packages
Requires:       dnf = %{version}-%{release}
%if %{with as_yum}
Obsoletes:      dnf-yum < %{version}-%{release}
Obsoletes:      yum < 4.0.0
Provides:       dnf-yum = %{version}-%{release}
# SUSE-specific split up of yum-utils features obsoleted by DNF itself...
%global yum_replaces() \
Obsoletes:      %{1} < 4.0.0 \
Provides:       %{1} = %{version}-%{release}

%yum_replaces  yum-aliases
%yum_replaces  yum-allowdowngrade
%yum_replaces  yum-basearchonly
%yum_replaces  yum-downloadonly
%yum_replaces  yum-fastestmirror
%yum_replaces  yum-priorities
%yum_replaces  yum-protect-packages
%yum_replaces  yum-protectbase
%yum_replaces  yum-refresh-updatesd
%yum_replaces  yum-tsflags

# yum-utils plugins with no replacement
Conflicts:      yum-filter-data
Conflicts:      yum-list-data
Conflicts:      yum-tmprepo
Conflicts:      yum-upgrade-helper
Conflicts:      yum-verify
%else
Conflicts:      yum
%endif

%description -n %{yum_subpackage_name}
As a Yum CLI compatibility layer, it supplies %{_bindir}/yum redirecting to DNF.

%package -n python3-dnf
Summary:        Python 3 interface to DNF
Group:          System/Packages
BuildRequires:  python3-curses
BuildRequires:  python3-devel
BuildRequires:  python3-gpg
BuildRequires:  python3-hawkey >= %{hawkey_version}
BuildRequires:  python3-libcomps >= %{libcomps_version}
BuildRequires:  python3-libmodulemd >= %{libmodulemd_version}
BuildRequires:  python3-nose
BuildRequires:  python3-rpm >= %{rpm_version}
Recommends:     (python3-dbus-python if NetworkManager)
Requires:       deltarpm
Requires:       dnf-data = %{version}-%{release}
Requires:       python3-curses
Requires:       python3-gpg
Requires:       python3-hawkey >= %{hawkey_version}
Requires:       python3-libcomps >= %{libcomps_version}
Requires:       python3-libmodulemd >= %{libmodulemd_version}
Requires:       python3-rpm >= %{rpm_version}
Recommends:     bash-completion
# DNF 2.0 doesn't work with old plugins
Conflicts:      python3-dnf-plugins-core < %{min_plugins_core}
Conflicts:      python3-dnf-plugins-extras-common < %{min_plugins_extras}
# Python 2 subpackage is no longer provided
Obsoletes:      python2-dnf < 4.0.10

%description -n python3-dnf
This package provides the Python 3 interface to DNF.

%lang_package

%package automatic
Summary:        Alternative CLI to "dnf upgrade" suitable for automatic, regular execution
Group:          System/Packages
BuildRequires:  systemd-rpm-macros
Requires:       dnf = %{version}-%{release}
%{?systemd_ordering}

%description automatic
Alternative CLI to "dnf upgrade" suitable for automatic, regular execution.

%prep
%autosetup -p1

# Fix sphinx-build run...
sed -e "s/sphinx-build-3/sphinx-build-%{python3_version}/" -i doc/CMakeLists.txt

%build
%cmake -DPYTHON_DESIRED:FILEPATH=%{__python3}
%make_build
make doc-man

%install
pushd ./build
%make_install
popd

%find_lang %{name}

mkdir -p %{buildroot}%{confdir}/repos.d
mkdir -p %{buildroot}%{confdir}/vars
mkdir -p %{buildroot}%{pluginconfpath}
mkdir -p %{buildroot}%{py3pluginpath}
mkdir -p %{buildroot}%{persistdir}
mkdir -p %{buildroot}%{_sharedstatedir}
ln -sf %{persistdir} %{buildroot}%{_sharedstatedir}/%{name}
mkdir -p %{buildroot}%{_localstatedir}/log
mkdir -p %{buildroot}%{_var}/cache/dnf
touch %{buildroot}%{_localstatedir}/log/%{name}.log

ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/dnf
mv %{buildroot}%{_bindir}/dnf-automatic-3 %{buildroot}%{_bindir}/dnf-automatic
ln -sr %{buildroot}%{_bindir}/dnf-3 %{buildroot}%{_bindir}/yum

%if %{with as_yum}
mkdir -p %{buildroot}%{_sysconfdir}/yum
ln -sr  %{buildroot}%{confdir}/%{name}.conf %{buildroot}%{_sysconfdir}/yum/yum.conf
ln -sr  %{buildroot}%{pluginconfpath} %{buildroot}%{_sysconfdir}/yum/pluginconf.d
ln -sr  %{buildroot}%{confdir}/protected.d %{buildroot}%{_sysconfdir}/yum/protected.d
ln -sr  %{buildroot}%{confdir}/repos.d %{buildroot}%{_sysconfdir}/yum/repos.d
ln -sr  %{buildroot}%{confdir}/vars %{buildroot}%{_sysconfdir}/yum/vars
%else
# We don't want this just yet...
rm -f %{buildroot}%{confdir}/protected.d/yum.conf
%endif

# This file is not used...
rm -f %{buildroot}%{confdir}/dnf-strict.conf

# We don't have ABRT/libreport in openSUSE
rm -rf %{buildroot}%{_sysconfdir}/libreport

%if %{with tests}
%check
pushd ./build
make ARGS="-V" test
popd
%endif

%files
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/dnf
%{_mandir}/man8/dnf.8*
%{_mandir}/man8/yum2dnf.8*
%{_mandir}/man7/dnf.modularity.7*
%{_mandir}/man5/dnf-transaction-json.5*
%dir %{_var}/cache/dnf
%{_unitdir}/dnf-makecache.service
%{_unitdir}/dnf-makecache.timer

%files lang -f %{name}.lang

%files data
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%dir %{confdir}
%dir %{pluginconfpath}
%dir %{confdir}/aliases.d
%dir %{confdir}/protected.d
%dir %{confdir}/repos.d
%dir %{confdir}/vars
%config(noreplace) %{confdir}/%{name}.conf
%config(noreplace) %{confdir}/aliases.d/zypper.conf
%config(noreplace) %{confdir}/protected.d/%{name}.conf
%config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%ghost %{_localstatedir}/log/hawkey.log
%ghost %{_localstatedir}/log/%{name}.log
%ghost %{_localstatedir}/log/%{name}.librepo.log
%ghost %{_localstatedir}/log/%{name}.rpm.log
%ghost %{_localstatedir}/log/%{name}.plugin.log
%dir %{persistdir}
%ghost %{persistdir}/groups.json
%ghost %{persistdir}/yumdb
%ghost %{persistdir}/history
%ghost %{_sharedstatedir}/dnf
%{_datadir}/bash-completion/completions/dnf
%{_mandir}/man5/dnf.conf.5.*
%{_tmpfilesdir}/dnf.conf

%files -n %{yum_subpackage_name}
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/yum
%{_mandir}/man8/yum.8.*
%{_mandir}/man8/yum-shell.8*
%{_mandir}/man5/yum.conf.5*
%{_mandir}/man1/yum-aliases.1*
%if %{with as_yum}
%dir %{_sysconfdir}/yum
%{_sysconfdir}/yum/yum.conf
%{_sysconfdir}/yum/pluginconf.d
%{_sysconfdir}/yum/protected.d
%{_sysconfdir}/yum/repos.d
%{_sysconfdir}/yum/vars
%config(noreplace) %{confdir}/protected.d/yum.conf
%endif

%files -n python3-dnf
%license COPYING PACKAGE-LICENSING
%doc AUTHORS README.rst
%{_bindir}/dnf-3
%exclude %{python3_sitelib}/dnf/automatic
%{python3_sitelib}/dnf/
%dir %{py3pluginpath}

%files automatic
%license COPYING PACKAGE-LICENSING
%doc AUTHORS
%{_bindir}/%{name}-automatic
%config(noreplace) %{confdir}/automatic.conf
%{_mandir}/man8/%{name}-automatic.8.*
%{_unitdir}/%{name}-automatic.service
%{_unitdir}/%{name}-automatic.timer
%{_unitdir}/%{name}-automatic-notifyonly.service
%{_unitdir}/%{name}-automatic-notifyonly.timer
%{_unitdir}/%{name}-automatic-download.service
%{_unitdir}/%{name}-automatic-download.timer
%{_unitdir}/%{name}-automatic-install.service
%{_unitdir}/%{name}-automatic-install.timer
%{python3_sitelib}/%{name}/automatic

%post
%systemd_post %{name}-makecache.timer

%preun
%systemd_preun %{name}-makecache.timer

%postun
%systemd_postun_with_restart %{name}-makecache.timer

%post automatic
%systemd_post %{name}-automatic.timer %{name}-automatic-notifyonly.timer %{name}-automatic-download.timer %{name}-automatic-install.timer

%preun automatic
%systemd_preun %{name}-automatic.timer %{name}-automatic-notifyonly.timer %{name}-automatic-download.timer %{name}-automatic-install.timer

%postun automatic
%systemd_postun_with_restart %{name}-automatic.timer %{name}-automatic-notifyonly.timer %{name}-automatic-download.timer %{name}-automatic-install.timer

%pretrans -n %{name}-data -p <lua>
-- Migrate DNF state data to /usr/lib/sysimage if it is still in /var/lib
oldpersistdir = "%{_sharedstatedir}/%{name}"
newpersistdir = "%{persistdir}"
chkst = posix.stat(oldpersistdir)
if chkst and chkst.type == "directory" then
  status = os.rename(oldpersistdir, newpersistdir)
  if status then
    posix.symlink(oldpersistdir, newpersistdir)
  end
end

%post -n %{name}-data
# Complete migration of DNF state data to /usr/lib/sysimage
if [ ! -L "%{_sharedstatedir}/%{name}" ]; then
   ln -sr %{persistdir} %{_sharedstatedir}/%{name}
fi

%if %{with as_yum}
%pretrans -n %{yum_subpackage_name} -p <lua>
-- Backup all legacy YUM package manager configuration subdirectories if they exist
yumconfpath = "%{_sysconfdir}/yum"
chkst = posix.stat(yumconfpath)
if chkst and chkst.type == "directory" then
  yumdirs = {"%{_sysconfdir}/yum/pluginconf.d", "%{_sysconfdir}/yum/protected.d", "%{_sysconfdir}/yum/repos.d", "%{_sysconfdir}/yum/vars"}
  for num,path in ipairs(yumdirs)
  do
    st = posix.stat(path)
    if st and st.type == "directory" then
      status = os.rename(path, path .. ".rpmmoved")
      if not status then
        suffix = 0
        while not status do
          suffix = suffix + 1
          status = os.rename(path .. ".rpmmoved", path .. ".rpmmoved." .. suffix)
        end
        os.rename(path, path .. ".rpmmoved")
      end
    end
  end
end
%endif

%changelog
* Wed Feb  3 2021 Neal Gompa <ngompa13@gmail.com>
- Update to version 4.6.0
  + Log scriptlets output also for API users (rh#1847340)
  + Fix module remove --all when no match spec (rh#1904490)
  + yum.misc.decompress() to handle uncompressed files (rh#1895059)
  + Make an error message more informative (rh#1814831)
  + Add deprecation notice to help messages of deplist
  + Remove Base._history_undo_operations() as it was replaced with transaction_sr code
  + cli/output: Return number of listed packages from listPkgs()
  + Clean up history command error handling
  + [doc] Describe install with just a name and obsoletes (rh#1902279)
  + Add api function fill_sack_from_repos_in_cache to allow loading a repo cache with repomd and (solv file or primary xml) only (rh#1865803)
  + Packages installed/removed via DNF API are logged into dnf.log (rh#1855158)
  + Support comps groups in history redo (rh#1657123, rh#1809565, rh#1809639)
  + Support comps groups in history rollback (rh#1657123, rh#1809565, rh#1809639)
  + Support comps groups in history undo (rh#1657123, rh#1809565, rh#1809639)
  + New optional parameter for filter_modules enables following modular obsoletes based on a config option module_obsoletes
  + Add get_header() method to the Package class (rh#1876606)
  + Fix documentation of globs not supporting curly brackets (rh#1913418)
* Thu Jan 28 2021 Cameron Rapp <camspam@redhyena.net>
- Fix a typo.
* Sun Dec  6 2020 Neal Gompa <ngompa13@gmail.com>
- Update to version 4.5.2
  + Change behaviour of Package().from_repo
  + Add a get_current() method to SwdbInterface
  + Add `from_repo` attribute for Package class (rh#1898968, rh#1879168)
  + Correct description of Package().reponane attribute
  + Add unittest for new API
  + Make rotated log file (mode, owner, group) match previous log settings (rh#1894344)
  + [doc] Improve description of modular filtering
  + [doc] add documentation for from_repo
  + [doc] deprecated alias for dnf repoquery --deplist <deplist_option-label>
  + New config option module_allow_stream_switch allows switching enabled streams
* Sun Nov 29 2020 Neal Gompa <ngompa13@gmail.com>
- Update to version 4.4.2
  + Warn about key retrieval over http
  + Fix --setopt=cachedir writing outside of installroot
  + Add vendor to dnf API (rh#1876561)
  + Add allow_vendor_change option (rh#1788371) (rh#1788371)
- Rename dnf-conf package to dnf-data, in line with upstream
* Sat Oct 24 2020 Neal Gompa <ngompa13@gmail.com>
- Update to version 4.4.0
  + Handle empty comps group name (rh#1826198)
  + Remove dead history info code (rh#1845800)
  + Improve command emmitter in dnf-automatic
  + Enhance --querytags and --qf help output
  + [history] add option --reverse to history list (rh#1846692)
  + Add logfilelevel configuration (rh#1802074)
  + Don't turn off stdout/stderr logging longer than necessary (rh#1843280)
  + Mention the date/time that updates were applied
  + [dnf-automatic] Wait for internet connection (rh#1816308)
  + [doc] Enhance repo variables documentation (rh#1848161, rh#1848615)
  + Add librepo logger for handling messages from librepo (rh#1816573)
  + [doc] Add package-name-spec to the list of possible specs
  + [doc] Do not use <package-nevr-spec>
  + [doc] Add section to explain -n, -na and -nevra suffixes
  + Add alias 'ls' for list command
  + remove log_lock.pid after reboot (rh#1863006)
  + comps: Raise CompsError when removing a non-existent group
  + Add methods for working with comps to RPMTransactionItemWrapper
  + Implement storing and replaying a transaction
  + Log failure to access last makecache time as warning
  + [doc] Document Substitutions class
  + Dont document removed attribute ``reports`` for get_best_selector
  + Change the debug log timestamps from UTC to local time
* Thu Jul 16 2020 Thorsten Kukuk <kukuk@suse.com>
- Use systemd_ordering instead of sytemd_requires, we don't want
  systemd in our containers.
* Tue Jul  7 2020 Neal Gompa <ngompa13@gmail.com>
- Update to version 4.2.23
  + Fix completion helper if solv files not in roon cache (rh#1714376)
  + Add bash completion for 'dnf module' (rh#1565614)
  + Check command no longer reports  missing %%pre and %%post deps (rh#1543449)
  + Check if arguments can be encoded in 'utf-8'
  + [doc] Remove incorrect information about includepkgs (rh#1813460)
  + Fix crash with "dnf -d 6 repolist" (rh#1812682)
  + Do not print the first empty line for repoinfo
  + Redirect logger and repo download progress when --verbose
  + Respect repo priority when listing packages (rh#1800342)
  + [doc] Document that list and info commands respect repo priority
  + [repoquery] Do not protect running kernel for --unsafisfied (rh#1750745)
  + Remove misleading green color from the "broken dependencies" lines (rh#1814192)
  + [doc] Document color options
  + Fix behavior of install-n, autoremove-n, remove-n, repoquery-n
  + Fix behavior of localinstall and list-updateinfo aliases
  + Add updated field to verbose output of updateinfo list (rh#1801092)
  + Add comment option to transaction (rh#1773679)
  + Add new API for handling gpg signatures (rh#1339617)
  + Verify GPG signatures when running dnf-automatic (rh#1793298)
  + Fix up Conflicts: on python-dnf-plugins-extras
  + [doc] Move yum-plugin-post-transaction-actions to dnf-plugins-core
  + Remove args "--set-enabled", "--set-disabled" from DNF (rh#1727882)
  + Search command is now alphabetical (rh#1811802)
  + Fix downloading packages with full URL as their location
  + repo: catch libdnf.error.Error in addition to RuntimeError in load() (rh#1788182)
  + History table to max size when redirect to file (rh#1786335, rh#1786316)
* Thu Feb 27 2020 Neal Gompa <ngompa13@gmail.com>
- Update to version 4.2.19
  + List arguments: only first empty value is used (rh#1788154)
  + Report missing profiles or default as broken module (rh#1790967)
  + repoquery: fix rich deps matching by using provide expansion from libdnf (rh#1534123)
  + [documentation] repoquery --what* with  multiple arguments (rh#1790262)
  + Format history table to use actual terminal width (rh#1786316)
  + Update `dnf alias` documentation
  + Handle custom exceptions from libdnf
  + Fix _skipped_packages to return only skipped (rh#1774617)
  + Add setter for tsi.reason
  + Add new hook for commands: Run_resolved
  + Add doc entry: include url (RhBug 1786072)
  + Clean also .yaml repository metadata
  + New API function base.setup_loggers() (rh#1788212)
  + Use WantedBy=timers.target for all dnf timers (rh#1798475)
* Sun Jan 19 2020 Neal Gompa <ngompa13@gmail.com>
- Update to version 4.2.18
  + [doc] Remove note about user-agent whitelist
  + Do a substitution of variables in repo_id (rh#1748841)
  + Respect order of config files in aliases.d (rh#1680489)
  + Unify downgrade exit codes with upgrade (rh#1759847)
  + Improve help for 'dnf module' command (rh#1758447)
  + Add shell restriction for local packages (rh#1773483)
  + Fix detection of the latest module (rh#1781769)
  + Document the retries config option only works for packages (rh#1783041)
  + Sort packages in transaction output by nevra (rh#1773436)
  + Honor repo priority with check-update (rh#1769466)
  + Strip '\' from aliases when processing (rh#1680482)
  + Print the whole alias definition in case of infinite recursion (rh#1680488)
  + Add support of commandline packages by repoquery (rh#1784148)
  + Running with tsflags=test doesn't update log files
  + Restore functionality of remove --oldinstallonly
  + Allow disabling individual aliases config files (rh#1680566)
* Sun Dec  1 2019 Neal Gompa <ngompa13@gmail.com>
- Update to version 4.2.17
  + Set default to skip_if_unavailable=false (rh#1679509)
  + Fix package reinstalls during yum module remove (rh#1700529)
  + Fail when "-c" option is given nonexistent file (rh#1512457)
  + Reuse empty lock file instead of stopping dnf (rh#1581824)
  + Propagate comps 'default' value correctly (rh#1674562)
  + Better search of provides in /(s)bin/ (rh#1657993)
  + Add detection for armv7hcnl (rh#1691430)
  + Fix group install/upgrade when group is not available (rh#1707624)
  + Report not matching plugins when using --enableplugin/--disableplugin
    (rh#1673289, rh#1467304)
  + Add support of modular FailSafe (rh#1623128)
  + Replace logrotate with build-in log rotation for dnf.log and dnf.rpm.log
    (rh#1702690)
  + Enhance synchronization of rpm transaction to swdb
  + Accept multiple specs in repoquery options (rh#1667898)
  + Prevent switching modules in all cases (rh#1706215)
  + [history] Don't store failed transactions as succeeded
  + [history] Do not require root for informative commands
  + [dnssec] Fix UnicodeWarning when using new rpm (rh#1699650)
  + Print rpm error messages during transaction (rh#1677199)
  + Report missing default profile as an error (rh#1669527)
  + Apply excludes before modular excludes (rh#1709453)
  + Improve help for command line arguments (rh#1659328)
  + [doc] Describe a behavior when plugin is removed (rh#1700741)
  + Add new modular API method ModuleBase.get_modules
  + Mark features used by ansible, anaconda and subscription-manager as an API
  + Prevent printing empty Error Summary (rh#1690414)
  + [doc] Add user_agent and countme options
  + Improve modularity documentation (rh#1730162, rh#1730162, rh#1730807, rh#1734081)
  + Fix detection whether system is running on battery (used by metadata caching timer) (rh#1498680)
  + New repoquery queryformat: %%{reason}
  + Print rpm errors during test transaction (rh#1730348)
  + Fix: --setopt and repo with dots
  + Fix incorrectly marked profile and stream after failed rpm transaction check (rh#1719679)
  + Show transaction errors inside dnf shell (rh#1743644)
  + Don't reinstall modified packages with the same NEVRA (rh#1644241)
  + dnf-automatic now respects versionlock excludes (rh#1746562)
  + Fix downloading local packages into destdir (rh#1727137)
  + Report skipped packages with identical nevra only once (rh#1643109)
  + Restore functionality of dnf remove --duplicates (rh#1674296)
  + Improve API documentation
  + Document NEVRA parsing in the man page
  + Do not wrap output when no terminal (rh#1577889)
  + Allow to ship alternative dnf.conf (rh#1752249)
  + Don't check if repo is expired if it doesn't have loaded metadata (rh#1745170)
  + Remove duplicate entries from "dnf search" output (rh#1742926)
  + Set default value of repo name attribute to repo id (rh#1669711)
  + Allow searching in disabled modules using "dnf module provides" (rh#1629667)
  + Group install takes obsoletes into account (rh#1761137)
  + Improve handling of vars
  + Do not load metadata for repolist commands (rh#1697472, rh#1713055, rh#1728894)
  + Don't show older install-only pkgs updates in updateinfo (rh#1649383, rh#1728004)
  + Add --ids option to the group command (rh#1706382)
  + Add --with_cve and --with_bz options to the updateinfo command (rh#1750528)
  + Make DNF compatible with FIPS mode (rh#1762032)
  + Return always alphabetically sorted modular profiles
  + Enable versionlock for check-update command (rh#1750620)
  + Add error message when no active modules matched (rh#1696204)
  + Log mirror failures as warning when repo load fails (rh#1713627)
  + dnf-automatic: Change all systemd timers to a fixed time of day (rh#1754609)
  + DNF can use config from the remote location (rh#1721091)
  + [doc] update reference to plugin documentation (rh#1706386)
  + [yum compatibility] Report all packages in repoinfo
  + [doc] Add definition of active/inactive module stream
  + repoquery: Add a switch to disable modular excludes
  + Report more informative messages when no match for argument (rh#1709563)
  + [doc] Add description of excludes in dnf
  + Report more descriptive message when removed package is excluded
  + Add module repoquery command
  + Fix assumptions about ARMv8 and the way the rpm features work (rh#1691430)
  + Add Requires information into module info commands
  + Enhance inheritance of transaction reasons (rh#1672618, rh#1769788)
- Rename dnf-yum package to yum and have it replace removed yum package on Tumbleweed
* Fri May 10 2019 Neal Gompa <ngompa13@gmail.com>
- Update to version 4.2.6
  + Turn on debug logging only if debuglevel is greater than 2 (rh#1355764, rh#1580022)
  + Fix issues with terminal hangs when attempting bash completion (rh#1702854)
  + Better detecting of file provides (rh#1702621)
  + Rename man page from dnf.automatic to dnf-automatic to match command name (rh#1703609)
- Drop patch included in this release
  * 0001-Python2-3-compatibility-for-exceptions-representatio.patch
* Fri Apr 26 2019 Neal Gompa <ngompa13@gmail.com>
- Update to version 4.2.5
  + Fix multilib obsoletes (rh#1672947)
  + Do not remove group package if other packages depend on it
  + Remove duplicates from "dnf list" and "dnf info" outputs
  + Installroot now requires absolute path
  + Allow globs in setopt in repoid part
  + Fix formatting of message about free space required
  + [doc] Add info of relation update_cache with fill_sack (rh#1658694)
  + Fix installation failiure when duplicate RPMs are specified (rh#1687286)
  + Add command abbreviations (rh#1634232)
  + Allow plugins to terminate dnf (rh#1701807)
  + Fix installation of bash completion helper (rh#1695853)
- Drop patches that are part of this release
  * 0001-Add-command-abbreviations-RhBug-1634232.patch
  * 0002-CMake-Actually-install-aliases.patch
  * 0001-Fix-the-installation-of-completion_helper.py.patch
- Backport fix for rendering exception messages in Python 3
  * 0001-Python2-3-compatibility-for-exceptions-representatio.patch
* Sat Apr 20 2019 Neal Gompa <ngompa13@gmail.com>
- Ship systemd units and enable dnf-automatic subpackage
- Backport fix to reintroduce subcommand abbreviations (rh#1634232)
  * Patch: 0001-Add-command-abbreviations-RhBug-1634232.patch
  * Patch: 0002-CMake-Actually-install-aliases.patch
- Backport fix to correctly install the bash completion helper (rh#1695853)
  * Patch: 0001-Fix-the-installation-of-completion_helper.py.patch
* Sun Mar 31 2019 Neal Gompa <ngompa13@gmail.com>
- Update to version 4.2.2
  + Allow to enable modules that break default modules (rh#1648839)
  + Enhance documentation - API examples
  + Add --nobest option
  + Do not allow direct module switch (rh#1669491)
  + Use improved config parser that preserves order of data
  + Fix alias list command (rh#1666325)
  + Update documentation: implemented plugins; options; deprecated commands (rh#1670835, rh#1673278)
  + Support zchunk (".zck") compression
  + Fix behavior  of ``--bz`` option when specifying more values
  + Follow RPM security policy for package verification
  + Update modules regardless of installed profiles
  + Fix ``list --showduplicates`` (rh#1655605)
  + [conf] Use environment variables prefixed with DNF_VAR_
  + Enhance documentation of --whatdepends option (rh#1687070)
  + Allow adjustment of repo from --repofrompath (rh#1689591)
  + Document cachedir option (rh#1691365)
  + Retain order of headers in search results (rh#1613860)
  + Solve traceback with the "dnf install @module" (rh#1688823)
- Drop upstreamed patch that is part of this release
  * 0001-doc-Use-the-correct-sphinx-build-binary-for-Python-2.patch
* Thu Feb  7 2019 Jan Engelhardt <jengelh@inai.de>
- Reduce generated boilerplate by joining %%systemd_* calls.
* Thu Feb  7 2019 Neal Gompa <ngompa13@gmail.com>
- Rebase to version 4.0.10:
  + Migrated large amounts of code to libdnf
  + Add support for RH/Fedora modules
  + Migrate from YUMDB to new SWDB
  + Add dnssec extension for repodata
  + Add support for aliases
- Drop Python 2 subpackage
- Drop unneeded patches
  * 0001-Add-additional-default-distroverpkg-and-installonlyp.patch
  * dnf-2.6.3-Switch-default-reposdir-to-etc-dnf-repos.d.patch
  * dnf-2.7.5-Fix-detection-of-Python-2.patch
- Add patch to fix detecting Sphinx in a Python 3 only build
  * 0001-doc-Use-the-correct-sphinx-build-binary-for-Python-2.patch
* Mon Apr 30 2018 Neal Gompa <ngompa13@gmail.com>
- Re-enable boolean dependencies now that Leap 15.0 and Tumbleweed
  both only use rpm-md repository metadata, which supports this
  properly.
- Adjust changes entries to use full author identities
* Sat Jan 20 2018 Neal Gompa <ngompa13@gmail.com>
- Fix build-time detection of Python 2
  * Add patch: dnf-2.7.5-Fix-detection-of-Python-2.patch
* Thu Jan  4 2018 Neal Gompa <ngompa13@gmail.com>
- Ensure DNF can recognize SUSE distro-release and kernel packages properly
  * Add patch: 0001-Add-additional-default-distroverpkg-and-installonlyp.patch
* Mon Nov 13 2017 Neal Gompa <ngompa13@gmail.com>
- Update to version 2.7.5:
  + Improved performance for excludes and includes handling (rh#1500361)
  + Fixed problem of handling checksums for local repositories (rh#1502106)
  + Fix traceback when using dnf.Base.close()
- Bump required pythonX-hawkey version
* Tue Oct 10 2017 Neal Gompa <ngompa13@gmail.com>
- Update to version 2.7.3:
  + Added new option '--comment=<comment>' that adds a comment to
    transaction in history
  + Added 'pre_configure()' method for plugins and commands to
    configure dnf before repos are loaded (rh#1212341)
  + 'dnf.Base.pre_configure_plugin()' configure plugins by running
    their 'pre_configure()' method (rh#1212341)
  + Support '--advisory=' with install (rh#1461171)
- Bump required pythonX-hawkey version as some APIs moved to libdnf
- Purge libreport configuration files instead of using exclude
* Tue Sep  5 2017 Neal Gompa <ngompa13@gmail.com>
- Add missing pythonX-curses Requires
* Tue Aug 29 2017 Dominique Leuenberger <dleuenberger@suse.com>
- Disable the boolean dependencies: this is a hack (sorry) as none
  of the released products support this in the susetags metadata,
  which resulted in no distro being able to add the TW repo. Once
  we migrate to the new prod builder, this can be re-enabled.
* Fri Aug 18 2017 Neal Gompa <ngompa13@gmail.com>
- Add dnf-lang subpackage for lang content
- Downgrade logrotate from Requires to Recommends in dnf-conf subpackage
- Switch (currently unused) BR from systemd-devel to systemd-rpm-macros
  as we only need macros
- Delete commented out BR on python-sphinx_rtd_theme as it's definitely
  not needed
* Sun Aug 13 2017 Neal Gompa <ngompa13@gmail.com>
- Create /etc/dnf/repos.d on install
* Sun Aug 13 2017 Neal Gompa <ngompa13@gmail.com>
- Always build with Python 3 support
* Sun Aug 13 2017 Neal Gompa <ngompa13@gmail.com>
- Disable systemd units and do not install dnf-automatic by default
* Sun Aug 13 2017 Neal Gompa <ngompa13@gmail.com>
- Switch default reposdir to /etc/dnf/repos.d
  * Add patch: dnf-2.6.3-Switch-default-reposdir-to-etc-dnf-repos.d.patch
* Sun Aug 13 2017 Neal Gompa <ngompa13@gmail.com>
- Initial packaging based on Mageia and Fedora packages
