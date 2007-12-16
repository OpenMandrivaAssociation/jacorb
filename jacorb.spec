# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

# If you want repolib package to be built,
# issue the following: 'rpmbuild --with repolib'

%define gcj_support 1

%define _with_repolib 1

%define with_repolib %{?_with_repolib:1}%{!?_with_repolib:0}
%define without_repolib %{!?_with_repolib:1}%{?_with_repolib:0}

%define repodir %{_javadir}/repository.jboss.com/jacorb/2.3.0jboss.patch4-brew
%define repodirlib %{repodir}/lib
%define repodirsrc %{repodir}/src

%define shortname jacorb

%define section devel

Summary:        Free Java implementation of OMG's CORBA standard
URL:            http://www.jacorb.org/
Source0:        http://www.jacorb.org/releases/2.3.0/JacORB-2.3.0-src.zip
Source1:        jacorb-jboss-component-info.xml
#Source2:       http://repository.jboss.com/jacorb/2.3.0jboss.patch3/resources/CSI.idl
#Source3:       http://repository.jboss.com/jacorb/2.3.0jboss.patch3/resources/CosTransactions.idl
Source4:        http://repository.jboss.com/jacorb/2.3.0jboss.patch3/resources/jacorb.properties
Source5:        http://repository.jboss.com/jacorb/2.3.0jboss.patch3/resources/orb.idl
Source6:        jacorb-idl-compiler-2.2.4.pom
Patch0:         jacorb-2.3.0-notification-build_xml.patch
Patch1:         jacorb-2.3.0-version.patch
# The size of a chunk should not include any bytes of padding that might have
# been added after the chunk for alignment purposes. This patch allows JacORB 
# to interoperate with the ORB in Sun's JDK 1.5 with chunking of custom RMI
# valuetypes enabled (jacorb.interop.chunk_custom_rmi_valuetypes=on), as it 
# should be per the CORBA spec. 
Patch2:         jacorb-2.3.0-chunk_size.patch
# In handle_chunking: change to distinguish a null value tag from
# a chunk size tag (the latter must be positive).
# In read_untyped_value and readChunkSizeTag: changes for correctness (to 
# ensure that chunk_end_pos is set to -1 if we are not within a chunk) and 
# for clarity.
Patch3:         jacorb-2.3.0-null_value_tag.patch
# Fix for bug #782 in JacORB's bugzilla system:
# The creation of an SSLServerSocket fails when JacORB 2.3.0 uses the JSSE
# included in Sun's JDK 1.4 and later releases. The problem is in the wrapper
# class JSSEUtil, which causes an IllegalAccessException to be thrown.
Patch4:         jacorb-2.3.0-JSSE.patch
# Fix for bug #783 in JacORB's bugzilla system:
# Server throws CORBA.INTERNAL (ArrayIndexOutOfBoundsException) when a client
# uses an IOR with a component tagged with TAG_CSI_SEC_MECH_LIST. When the 
# current implementation of the method 
# org.jacorb.orb.iiop.IIOPProfile.getTLSPortFromCSIComponent finds an IOR
# component that is tagged with TAG_CSI_SEC_MECH_LIST and has a non-empty list
# of security mechanisms, it assumes that the first mechanism listed has a 
# transport component tagged with TAG_TLS_SEC_TRANS. It tries to access the 
# data of the presumed TLS_SEC_TRANS component, without first checking the 
# component's tag. If this tag is TAG_NULL_TAG rather than TAG_TLS_SEC_TRANS, 
# then an ArrayIndexOutOfBoundsException occurs.
Patch5:         jacorb-2.3.0-IIOP.patch
# Fix for NPE on shutdown
Patch6:         jacorb-2.3.0-IIOP_Shutdown.patch
Patch7:         jacorb-2.3.0-no-classpath-in-manifest.patch

Name:           jacorb
Version:        2.3.0
Release:        %mkrel 1.0.6
Epoch:          0
License:        LGPL
Group:          Development/Java
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch: noarch
%endif
BuildRequires:   java-rpmbuild >= 0:1.6
BuildRequires:   ant >= 0:1.6.5
BuildRequires:   antlr
BuildRequires:   concurrent
BuildRequires:   avalon-framework
BuildRequires:   excalibur-avalon-logkit
#BuildRequires:  backport-util-concurrent
BuildRequires:   jakarta-commons-collections
BuildRequires:   jakarta-commons-logging
BuildRequires:   tanukiwrapper
#BuildRequires:  picocontainer
BuildRequires:   xdoclet
BuildRequires:   xjavadoc
Requires:        jpackage-utils >= 0:1.6
Requires:        concurrent
Requires:        avalon-framework
Requires:        excalibur-avalon-logkit
Requires:        jakarta-commons-collections
Requires:        jakarta-commons-logging
Requires:        tanukiwrapper
#Optional:       picocontainer
BuildRoot:       %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
- high-performance, fully multithreaded ORB 
- IDL compiler, supports OMG IDL/Java language mapping 
  rev. 2.3, OBV 
- native IIOP, GIOP 1.2 and Bidirectional GIOP 
- POA (Portable Object Adapter) 
- AMI (Asynchronous Method Invocations) 
- ETF (Extensible Transport Framework) 
- POAMonitor, a GUI tools that lets you inspect your 
  object adapters (screenshot) 
- Dynamic Invocation Interface (DII) and Dynamic Skeleton 
  Interface (DSI) 
- Dynamic Management of Anys (DynAny) 
- Portable Interceptors (standard) 
- OMG Interoperable Naming Service 
- NameManager, a GUI browser for the name service 
  (requires Swing or JDK 1.2) (screenshot) 
- improved IIOP over SSL, includes KeyStoreManager 
- OMG Notification  and Event service 
- Transaction Service, Collection and Concurrency services 
- TradingService (supports trader links), an extension of 
  Mark Spruiell's free JTrader 
- CORBA 2.3 Code set support 
- Appligator, an IIOP proxy 
- Support for HTTP tunneling 
- Domain Manager, an object domain management service, 
  includes a domain browser GUI 
- Interface Repository 
- IRBrowser, a GUI front end for the Interface Repository
- Implementation Repository 
- Implementation Repository Manager, a GUI front end for 
  the Implementation Repository 
- IDL and Java source for all CORBA/COSS interfaces 
- examples and full source code included 
- 100% pure Java, JDK 1.3 and 1.4 compatible, also cooperates 
  with Sun's JDK 1.2 classes (releases prior to 1.4 are 
  compatible with JDK 1.1) 

ClassPath: antlr-2.7.2.jar:avalon-framework-4.1.5.jar:
logkit-1.2.jar:commons-collections-2.0.jar:commons-logging.jar:
wrapper-3.1.0.jar (see 'rpm --requires jacorb-jboss')
Note: To use on Java 1.4 add backport-util-concurrent.jar to the
ClassPath (from the RPM with the same name)
Note: To use the CORBA Notification Service add
picocontainer-1.2.jar to the ClassPath (from the 'picocontainer'
RPM).

%if %{with_repolib}
%package repolib
Summary:      Artifacts to be uploaded to a repository library
Group:        Development/Java

%description repolib
Artifacts to be uploaded to a repository library.
This package is not meant to be installed but so its contents
can be extracted through rpm2cpio
%endif

%package javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description javadoc
%{summary}

%package manual
Summary:        Documents for %{name}
Group:          Development/Java

%description manual
%{summary}

%package demo
Summary:        Usage examples for %{name}
Group:          Development/Java

%description demo
%{summary}

%prep
%setup -q -n JacORB
chmod -R go=u-w *
for j in $(find . -name "*.jar"); do
        rm $j
done

%patch0 -b .sav
%patch1 -b .sav
%patch2 -b .sav
%patch3 -b .sav
%patch4 -b .sav
%patch5 -b .sav
%patch6 -b .sav
%patch7 -p1

tag=`echo %{name}-%{version}-%{release} | sed 's|\.|_|g'`
sed -i "s/@TAG@/$tag/g" %{SOURCE1}

%{__perl} -pi -e 's/\r$//g' \
doc/HOWTO/HOWTO-WebLogic_integration.html \
doc/HOWTO/HOWTO-eclipse_integration.html \
doc/dds/style.css

%build
pushd lib
ln -sf $(build-classpath antlr) .
ln -sf $(build-classpath avalon-framework) .
#ln -sf $(build-classpath excalibur/avalon-framework-impl) .
#ln -sf $(build-classpath backport-util-concurrent) .
ln -sf $(build-classpath excalibur/avalon-logkit) .
#ln -sf $(build-classpath picocontainer) .
ln -sf $(build-classpath tanukiwrapper) .
pushd build
ln -sf $(build-classpath commons-collections) .
ln -sf $(build-classpath commons-logging) .
ln -sf $(build-classpath xdoclet/xdoclet) .
ln -sf $(build-classpath xdoclet/xdoclet-ejb-module) .
ln -sf $(build-classpath xdoclet/xdoclet-jboss-module) .
ln -sf $(build-classpath xdoclet/xdoclet-jmx-module) .
ln -sf $(build-classpath xdoclet/xdoclet-mx4j-module) .
ln -sf $(build-classpath xdoclet/xdoclet-web-module) .
ln -sf $(build-classpath xjavadoc) .
popd
popd
# Tests were not included with the 2.2.4 source zip
#pushd test/regression/lib
#ln -sf $(build-classpath easymock) .
#ln -sf $(build-classpath emma) .
#ln -sf $(build-classpath emma_ant) .
#ln -sf $(build-classpath junit) .
#popd

mkdir temp
#ant all doc
%{ant} convert.jdk5 jar idllib doc
for i in lib/*.jar ; do j=`basename $i` ; cp $i temp/${j/\.jar/_g.jar} ; done
%{ant} realclean
%{ant} -Ddebug=off convert.jdk5 jar idllib doc

%install
rm -rf $RPM_BUILD_ROOT

# remove DOS files
find . -name "*.exe" -exec rm {} \;
find . -name "*.bat" -exec rm {} \;

# jar
install -d -m 0755 $RPM_BUILD_ROOT%{_javadir}/%{name}
install -p -m 0644 lib/%{shortname}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{shortname}-%{version}.jar
install -p -m 0644 temp/%{shortname}_g.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/%{shortname}_g-%{version}.jar
install -p -m 0644 lib/idl.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/idl-%{version}.jar
install -p -m 0644 temp/idl_g.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/idl_g-%{version}.jar
(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done)

# pom
install -dm 0755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 0644 %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.jacorb-idl.pom
%add_to_maven_depmap org.jacorb jacorb-idl-compiler %{version} JPP/jacorb idl

# bin, etc, idl
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/bin
cp -pr bin/*   $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/bin
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/etc
cp -pr etc/*   $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/etc
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/idl
cp -pr idl/*   $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/idl

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr doc/api/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}
rm -rf doc/api

# manual
install -d -m 0755 $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/doc
cp index.html   $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}
cp -pr doc/*   $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/doc

# demo
install -d -m 0755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/demo


%if %{with_repolib}
        install -d -m 755 $RPM_BUILD_ROOT%{repodir}
        install -d -m 755 $RPM_BUILD_ROOT%{repodir}/resources
        install -d -m 755 $RPM_BUILD_ROOT%{repodirlib}
        install -m 755 %{SOURCE1} $RPM_BUILD_ROOT%{repodir}/component-info.xml
        install -d -m 755 $RPM_BUILD_ROOT%{repodirsrc}
        install -m 755 %{PATCH0} $RPM_BUILD_ROOT%{repodirsrc}
        install -m 755 %{PATCH1} $RPM_BUILD_ROOT%{repodirsrc}
        install -m 755 %{PATCH2} $RPM_BUILD_ROOT%{repodirsrc}
        install -m 755 %{PATCH3} $RPM_BUILD_ROOT%{repodirsrc}
        install -m 755 %{PATCH4} $RPM_BUILD_ROOT%{repodirsrc}
        install -m 755 %{PATCH5} $RPM_BUILD_ROOT%{repodirsrc}
        install -m 755 %{PATCH6} $RPM_BUILD_ROOT%{repodirsrc}
        install -m 755 %{SOURCE0} $RPM_BUILD_ROOT%{repodirsrc}
#        install -m 755 %{SOURCE2} $RPM_BUILD_ROOT%{repodir}/resources
        install -m 755 idl/omg/CSI.idl $RPM_BUILD_ROOT%{repodir}/resources
#        install -m 755 %{SOURCE3} $RPM_BUILD_ROOT%{repodir}/resources
        install -m 755 idl/omg/CosTransactions.idl $RPM_BUILD_ROOT%{repodir}/resources
        install -m 755 %{SOURCE4} $RPM_BUILD_ROOT%{repodir}/resources
        install -m 755 %{SOURCE5} $RPM_BUILD_ROOT%{repodir}/resources
        cp $RPM_BUILD_ROOT%{_javadir}/%{name}/idl_g.jar $RPM_BUILD_ROOT%{repodirlib}
        cp $RPM_BUILD_ROOT%{_javadir}/%{name}/%{shortname}_g.jar $RPM_BUILD_ROOT%{repodirlib}
        cp $RPM_BUILD_ROOT%{_javadir}/%{name}/%{shortname}.jar $RPM_BUILD_ROOT%{repodirlib}
        cp $RPM_BUILD_ROOT%{_javadir}/%{name}/idl.jar $RPM_BUILD_ROOT%{repodirlib}
        install -m 755 %{SOURCE0} $RPM_BUILD_ROOT%{repodirlib}
%endif

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_maven_depmap
%if %{gcj_support}
  %{update_gcjdb}
%endif

%postun
%update_maven_depmap
%if %{gcj_support}
  %{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
%{_javadir}/%{name}
%{_docdir}/%{name}-%{version}/doc/LICENSE
%dir %{_datadir}/%{name}-%{version}/bin
%attr(0755,root,root) %{_datadir}/%{name}-%{version}/bin/*
%{_datadir}/%{name}-%{version}/etc
%{_datadir}/%{name}-%{version}/idl
%{_datadir}/maven2/poms
%{_mavendepmapfragdir}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}

%files manual
%defattr(0644,root,root,0755)
%{_docdir}/%{name}-%{version}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}-%{version}/demo

%if %{with_repolib}
%files repolib
%defattr(0644,root,root,0755)
%{repodir}
%endif
