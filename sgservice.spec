%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global pypi_name sgservice

Name:			sgservice
Epoch:			1
Version:		XXX
Release:		XXX
Summary:		Service provides SG enabled volume management and data protection across clouds

License:		ASL 2.0
URL:   			https://github.com/Hybrid-Cloud/SG-Service
Source0:		https://github.com/Hybrid-Cloud/%{name}/%{name}-%{upstream_version}.tar.gz

BuildArch:		noarch

%description
Service provides SG enabled volume management and data protection across clouds

%package -n python-%{pypi_name}
Summary:          Service provides SG enabled volume management and data protection across clouds

BuildRequires:    python2-devel
BuildRequires:    python-setuptools
BuildRequires:    python-pbr
BuildRequires:    python-d2to1

Requires:         python-babel
Requires:         python-iso8601
Requires:         python-jsonschema
Requires:         python-keystoneauth1 >= 2.1.0
Requires:         python-oslo-i18n >= 2.1.0
Requires:         python-oslo-serialization >= 2.1.0
Requires:         python-oslo-utils >= 3.4.0
Requires:         python-prettytable
Requires:         python-pbr
Requires:         python-requests
Requires:         python-six >= 1.9.0
Requires:         python-simplejson


%description -n python-%{pypi_name}
Service provides SG enabled volume management and data protection across clouds

%prep
%setup -q -n %{name}-%{upstream_version}

# Remove bundled egg-info
rm -rf python_sgservice.egg-info

# Let RPM handle the requirements
rm -f {,test-}requirements.txt

%build
%{__python2} setup.py build

# Fix hidden-file-or-dir warnings
rm -fr html/.doctrees html/.buildinfo

%install
%{__python2} setup.py install -O1 --skip-build --root %{buildroot}

# Delete test
rm -fr %{buildroot}%{python-sitelib}/sgservice/tests

%files -n python-%{pypi_name}
%{_bindir}/sgs
%{python2_sitelib}/sgservice
%{python2_sitelib}/*.egg-info


%changelog
