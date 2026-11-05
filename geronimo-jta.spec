%global spec_name geronimo-jta_1.1_spec
%bcond_with javadoc

Name:		geronimo-jta
Version:	1.1.1
Release:	16
Summary:	J2EE JTA v1.1 API


License:	ASL 2.0
URL:		https://geronimo.apache.org/
# svn export http://svn.apache.org/repos/asf/geronimo/specs/tags/%{spec_name}-%{version}/
Source0:	%{spec_name}-%{version}.tar.bz

BuildArch:	noarch
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven
BuildOption(install):	--file-name %{name} --link %{spec_name} --link jta --alias javax.transaction:jta --alias org.eclipse.jetty.orbit:javax.transaction

# This pulls in almost all of the required java and maven stuff
BuildRequires:	geronimo-parent-poms
BuildRequires:	maven-resources-plugin

# Ensure a smooth transition from geronimo-specs
Provides:	jta = %{version}-%{release}
Obsoletes:	geronimo-specs <= 1.0-3.3
Obsoletes:	geronimo-specs-compat <= 1.0-3.3

%description
Java Transaction API (JTA) specifies standard Java interfaces between a
transaction manager and the parties involved in a distributed transaction
system: the resource manager, the application server, and the transactional
applications.

%if %{with javadoc}
%package javadoc
Summary:	API documentation for %{name}

BuildArch:	noarch

%endif
%if %{with javadoc}
%description javadoc
%{summary}.

%endif
%prep
%setup -q -n %{spec_name}-%{version}


%if %{with javadoc}
%pre javadoc
# workaround for rpm bug, can be removed in F-20
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%endif
%files -f .mfiles
%doc LICENSE.txt NOTICE.txt

%if %{with javadoc}
%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt NOTICE.txt


%endif
