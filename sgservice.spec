%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc %{!?_without_doc:1}%{?_without_doc:0}
%global pypi_name sgservice

Name:           sgservice
Epoch:          1
Version:        XXX
Release:        XXX
Summary:        Storage-Gateway Service

License:        ASL 2.0
URL:            https://github.com/Hybrid-Cloud/SG-Service
Source0:        https://github.com/Hybrid-Cloud/%{name}/%{name}-%{upstream_version}.tar.gz

Source1:        sgservice-dist.conf
Source2:        sgservice.logrotate
Source3:        sgservice.sudoers

Source10:       sgservice-api.service
Source11:       sgservice-controller.service
Source12:       sgservice-manage.service
Source13:       sgservice-proxy.service

BuildArch:      noarch
BuildRequires:  intltool
BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-pbr
BuildRequires:  python-d2to1
BuildRequires:  python-crypto
BuildRequires:  python-cryptography
BuildRequires:  python-sgservice-caaclient
BuildRequires:  python-decorator
BuildRequires:  python-cinderclient
BuildRequires:  python-glanceclient
BuildRequires:  python-greenlet
BuildRequires:  python-heatclient
BuildRequires:  python-iso8601
BuildRequires:  python-keystoneclient
BuildRequires:  python-keystonemiddleware
BuildRequires:  python-lxml
BuildRequires:  python-neutronclient
BuildRequires:  python-novaclient
BuildRequires:  python-oslo-cache
BuildRequires:  python-oslo-concurrency
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-context
BuildRequires:  python-oslo-db
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-messaging
BuildRequires:  python-osprofiler
BuildRequires:  python-oslo-middleware
BuildRequires:  python-oslo-policy
BuildRequires:  python-oslo-reports
BuildRequires:  python-oslo-serialization
BuildRequires:  python-oslo-service
BuildRequires:  python-oslo-utils
BuildRequires:  python-oslo-versionedobjects
BuildRequires:  PyYAML

Requires:       python-%{pypi_name} = %{epoch}:%{version}-%{release}

Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
Requires(pre):    shadow-utils

%description
SG-Service

%package -n python-%{pypi_name}
Summary:        SG-Service Code

Requires:       pyparsing >= 2.0.1
Requires:       python-anyjson
Requires:       python-babel
Requires:       python-crypto
Requires:       python-cryptography >= 1.0
Requires:       python-decorator
Requires:       python-eventlet >= 0.17.4
Requires:       python-glanceclient >= 1:2.0.0
Requires:       python-greenlet
Requires:       python-heatclient >= 0.6.0
Requires:       python-httplib2 >= 0.7.5
Requires:       python-iso8601 >= 0.1.9
Requires:       python-keystoneclient >= 1:1.6.0
Requires:       python-keystonemiddleware >= 4.0.0
Requires:       python-lxml >= 2.3
Requires:       python-migrate >= 0.9.6
Requires:       python-netaddr
Requires:       python-oauth2client >= 1.5.0
Requires:       python-os-brick >= 1.0.0
Requires:       python-oslo-cache >= 0.8.0
Requires:       python-oslo-concurrency >= 2.30
Requires:       python-oslo-config >= 3.4.0
Requires:       python-oslo-context >= 2.0.0
Requires:       python-oslo-db >= 4.1.0
Requires:       python-oslo-i18n >= 2.1.0
Requires:       python-oslo-log >= 1.14.0
Requires:       python-oslo-messaging >= 2.1.0
Requires:       python-oslo-middleware >= 3.0.0
Requires:       python-oslo-policy >= 0.5.0
Requires:       python-oslo-reports >= 0.6.0
Requires:       python-oslo-rootwrap >= 0.6.0
Requires:       python-oslo-serialization >= 2.1.0
Requires:       python-oslo-service >= 1.0.0
Requires:       python-oslo-utils >= 3.4.0
Requires:       python-oslo-versionedobjects >= 1.4.0
Requires:       python-osprofiler >= 1.1.0
Requires:       python-paramiko
Requires:       python-paste-deploy
Requires:       python-paste
Requires:       python-pbr
Requires:       python-requests
Requires:       python-retrying >= 1.2.3
Requires:       python-routes
Requires:       python-rtslib >= 2.1
Requires:       python-simplejson >= 2.2.0
Requires:       python-six >= 1.9.0
Requires:       python-sqlalchemy >= 1.0.10
Requires:       python-stevedore >= 1.5.0
Requires:       python-suds
Requires:       python-webob >= 1.2.3
Requires:       pytz
Requires:       grpcio >= 1.0.4
Requires:       netifaces >= 0.10.5
Requires:       pyparsing >= 2.2.0 
Requires:       python-cinderclient >= 2.0.1
Requires:       python-novaclient >= 7.1.0
Requires:       pymysql >= 0.7.10
Requires:       keystonemiddleware >= 4.2.0

%description -n python-%{pypi_name}
SG-Service Code


%package -n python-%{pypi_name}-tests
Summary:        SG-Service tests
Requires:       python-%{pypi_name} = %{epoch}:%{version}-%{release}

%description -n python-%{pypi_name}-tests
SG-Service tests

%prep
%setup -q -n sgservice-%{upstream_version}

find . \( -name .gitignore -o -name .placeholder \) -delete

find sgservice -name \*.py -exec sed -i '/\/usr\/bin\/env python/{d;q}' {} +

sed -i 's/%{version}.%{milestone}/%{version}/' PKG-INFO

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
#PYTHONPATH=. oslo-config-generator --config-file=etc/sgservice/sgservice-config-generator.conf

%{__python2} setup.py build

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Setup directories
install -d -m 750 %{buildroot}%{_sysconfdir}/sgservice
install -d -m 750 %{buildroot}%{_localstatedir}/log/sgservice
install -d -m 755 %{buildroot}%{_sharedstatedir}/sgservice

# Install config files
install -p -D -m 640 %{SOURCE1} %{buildroot}%{_datarootdir}/sgservice/sgservice-dist.conf
install -p -D -m 755 etc/sgservice.conf %{buildroot}%{_sysconfdir}/sgservice/sgservice.conf
install -p -D -m 755 etc/sgservice_api.conf %{buildroot}%{_sysconfdir}/sgservice/sgservice_api.conf
install -p -D -m 755 etc/sgservice_controller.conf %{buildroot}%{_sysconfdir}/sgservice/sgservice_controller.conf
install -p -D -m 755 etc/sgservice_proxy.conf %{buildroot}%{_sysconfdir}/sgservice/sgservice_proxy.conf
install -p -D -m 755 etc/api-paste.ini %{buildroot}%{_sysconfdir}/sgservice/api-paste.ini
install -p -D -m 755 etc/policy.json %{buildroot}%{_sysconfdir}/sgservice/policy.json

# Install initscripts for sgservice services
install -p -D -m 644 %{SOURCE10} %{buildroot}%{_unitdir}/sgservice-api.service
install -p -D -m 644 %{SOURCE11} %{buildroot}%{_unitdir}/sgservice-controller.service
install -p -D -m 644 %{SOURCE12} %{buildroot}%{_unitdir}/sgservice-manage.service
install -p -D -m 644 %{SOURCE13} %{buildroot}%{_unitdir}/sgservice-proxy.service

# Install sudoers
install -p -D -m 440 %{SOURCE3} %{buildroot}%{_sysconfdir}/sudoers.d/sgservice

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/sgservice

# INstall pid directory
install -d -m 755 %{buildroot}%{_localstatedir}/run/sgservice

# Remove unneeded in production stuff
rm -f %{buildroot}%{_bindir}/sgservice-debug
rm -fr %{buildroot}%{python2_sitelib}/run_tests.*
rm -f %{buildroot}/usr/share/doc/sgservice/README*

%pre -n python-%{pypi_name}
getent group sgservice >/dev/null || groupadd -r sgservice
if ! getent passwd sgservice >/dev/null; then
    useradd -r -g sgservice -G sgservice,nobody -d %{_sharedstatedir}/sgservice -s /sbin/nologin -c "SG-Service Daemons" sgservice
fi
exit 0

%post
%systemd_post sgservice-api
%systemd_post sgservice-controller
%systemd_post sgservice-manage
%systemd_post sgservice-proxy

%preun
%systemd_preun sgservice-api
%systemd_preun sgservice-controller
%systemd_preun sgservice-manage
%systemd_preun sgservice-proxy

%postun
%systemd_postun_with_restart sgservice-api
%systemd_postun_with_restart sgservice-controller
%systemd_postun_with_restart sgservice-manage
%systemd_postun_with_restart sgservice-proxy

%files
%dir %{_sysconfdir}/sgservice
%config(noreplace) %attr(-, root, sgservice) %{_sysconfdir}/sgservice/sgservice.conf
%config(noreplace) %attr(-, root, sgservice) %{_sysconfdir}/sgservice/sgservice_api.conf
%config(noreplace) %attr(-, root, sgservice) %{_sysconfdir}/sgservice/sgservice_controller.conf
%config(noreplace) %attr(-, root, sgservice) %{_sysconfdir}/sgservice/sgservice_proxy.conf
%config(noreplace) %attr(-, root, sgservice) %{_sysconfdir}/sgservice/api-paste.ini
%config(noreplace) %attr(-, root, sgservice) %{_sysconfdir}/sgservice/policy.json
%config(noreplace) %{_sysconfdir}/logrotate.d/sgservice
%config(noreplace) %{_sysconfdir}/sudoers.d/sgservice
%{_sysconfdir}/sgservice/rootwrap.d/
%attr(-, root, sgservice) %{_datadir}/sgservice/sgservice-dist.conf

%dir %attr(0750, sgservice, root) %{_localstatedir}/log/sgservice
%dir %attr(0755, sgservice, root) %{_localstatedir}/run/sgservice

%{_bindir}/sgservice-*
%{_unitdir}/*.service
%{_datarootdir}/sgservice

%defattr(-, sgservice, sgservice, -)
%dir %{_sharedstatedir}/sgservice

%files -n python-sgservice
%{?!_licensedir: %global license %%doc}
%license LICENSE
%{python2_sitelib}/sgservice
%{python2_sitelib}/sgservice-*.egg-info
%exclude %{python2_sitelib}/sgservice/tests

%files -n python-sgservice-tests
%license LICENSE
%{python2_sitelib}/sgservice/tests

%changelog
