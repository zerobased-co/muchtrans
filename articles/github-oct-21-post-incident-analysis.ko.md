title: 깃헙의 10월 21일 장애 사후 분석
source: https://blog.github.com/2018-10-30-oct21-post-incident-analysis/

#  10월 21일 장애 사후 분석

지난 주, 깃헙(GitHub)에 [문제가 발생](https://blog.github.com/2018-10-21-october21-incident-report/)해 24시간 11분 동안 제한된 서비스만 제공할 수 있었습니다. 일부 플랫폼은 영향 밖에 있었지만, 많은 내부 시스템이 영향을 받아 일관되지 않고 부정확한 정보를 표시하는 문제가 있었습니다. 최종적으로 어떠한 사용자 데이터도 잃어버리진 않았습니다. 하지만 데이터베이스 쓰기 작업에 대한 수 초간의 수동 조작은 아직 진행중입니다. 대부분의 문제는 웹훅 이벤트를 제공하지 못하거나 깃헙 페이지 사이트를 만들고 퍼블리싱하지 못하는 것이었습니다.

깃헙 구성원 모두는 이 사건이 일어난 것에 대해 여러분 한 분 한 분에게 진심으로 사과의 말씀을 드립니다. 깃헙에 대한 여러분의 신뢰를 잘 이해하고 고가용성 플랫폼을 구축하는 우리의 탄력적 시스템 구축 기술에 자부심도 가지고 있습니다. 이번 사건으로 여러분에게 실망을 드려 대단히 죄송합니다. 깃헙 플랫폼을 사용할 수 없었던 긴 시간동안 이로 인해 발생한 문제들을 저희가 되돌릴 수는 없겠지만, 문제의 원인과 이번 사고를 통해 저희가 배운 것들, 그리고 이런 일이 다시는 일어나지 않도록 회사 입장에서 취할 수 있는 조치에 대해 설명드리고 싶습니다.

## 사건 배경

사용자에게 노출되는 깃헙 서비스의 대부분은 저희의 자체 [데이터 센터](https://githubengineering.com/evolution-of-our-data-centers/)에서 동작하고 있습니다. 데이터 센터의 구성은 연산과 저장을 수행하는 여러 지역의 데이터 센터의 앞단에서 견고하고 유연한 엣지 네트워크를 제공하도록 설계되어 있습니다. 이렇게 설계된 물리적이며 논리적인 컴포넌트 위에 여러 층으로 구성된 견고함에도 불구하고, 여전히 일정 시간 동안 사이트가 서로 통신할 수 없을 수도 있습니다.

10월 21일 22:52 UTC에 망가진 100G 광통신 장비를 교체하는 정기 보수 작업으로 인해 미 동부 해안 네트워크 허브와 우리의 주 데이터 센터인 미 동부 데이터 센터간의 연결이 끊겼습니다. 양측의 연결은 43초만에 복구되었습니다만, 이 짧은 끊김으로 인해 24시간 11분간의 서비스 장애가 이어졌습니다.

![2개의 물리적 데이터 센터와 3개의 팝, 다양한 지역에 위치한 클라우드 사이의 직접 연결을 포함한 깃헙 네트워크의 개괄적 묘사](https://blog.github.com/assets/img/2018-10-25-oct21-post-incident-analysis/network-architecture.png)

예전에 저희가 어떻게 [MySQL으로 깃헙 메타데이터 저장하는지](https://githubengineering.com/orchestrator-github)와 [고가용성 MySQL 운영](https://githubengineering.com/mysql-high-availability-at-github)에 대해 논한 적이 있습니다. 깃헙은 수백 기가바이트에서 5 테라바이트에 이르는 다양한 크기의 여러 MySQL 클러스터를 여러 개의 읽기 복제본과 함께 운영하여 깃과 무관한 메타데이터를 저장하고 있습니다. 깃 오브젝트 저장소 외에 풀 리퀘스트와 이슈, 인증 관리, 백그라운드 작업 조율 외 다양한 기능들이 이에 해당합니다. 응용 프로그램의 여러 부분의 서로 다른 데이터들은 기능별 샤딩을 통해 나뉘어 여러 클러스터에 저장됩니다.

대규모 서비스에서의 성능 향상을 위해 응용 프로그램은 클러스터내 연관된 주 저장소(primary)에 직접 쓰지만, 대부분의 읽기 요청은 읽기 복제본에 위임하는 편입니다. MySQL 클러스터 구성 관리와 자동 복구를 위해 [Orchestrator](https://github.com/github/orchestrator)를 쓰고 있습니다. Orchestrator는 이 과정에서 여러 변수를 고려하여 동작하며, 합의를 위해 [Raft](https://raft.github.io/)를 기반으로 만들어졌습니다. Orchestrator는 응용 프로그램이 지원하지 못하는 수준의 구성이 가능하므로 Orchestrator의 설정을 응용 프로그램의 수준에 맞춰 운영하기 위해서는 주의가 필요합니다.

![일반적인 구성에서, 모든 응용 프로그램이 짧은 지연 시간으로 읽기를 수행하는 모습.](https://blog.github.com/assets/img/2018-10-25-oct21-post-incident-analysis/normal-topology.png)

## 사건 타임라인

### 2018년 10월 21일 22:52 UTC

위에서 설명한 것과 같이 네트워크가 나뉜동안, 주 데이터센터에서 동작하던 Orchestrator는 Raft의 합의 원칙에 따라 리더쉽 선택 취소 프로세스를 시작했습니다. 서부 해안 데이터센터와 동부 해안 공용 클라우드의 Orchestrator 노드들은 (합의에 필요한) 정족수를 채우고 서부 해안 데이터센터에 직접 데이터를 쓰도록 클러스터를 복구할 수 있었습니다. Orchestrator는 서부 해안 데이터베이스 클러스터 구성을 조직하기 시작했고, 연결이 복원되자마자 응용 프로그램들은 일제히 새롭게 선출된 서부 해안 쪽으로 데이터를 쓰기 시작했습니다.

동부 해안 데이터센터에 있는 데이터베이스 서버에는 아직 서부 해안 쪽으로 복제되지 않은 쓰기 작업들이 남아 있었습니다. 양쪽 데이터센터에 서로에게 있지 않은 쓰기 작업들이 남게된 것입니다. 이로 인해 동부 해안의 데이터센터에서는 주 데이터베이스 선정 작업이 실패하게 되었습니다.

### 2018년 10월 21일 22:54 UTC

내부 모니터링 시스템이 우리의 시스템에 여러 문제가 발생했다고 알리기 시작했습니다. 이 때부터 많은 엔지니어들이 몰려 들어오는 알림을 분류하고 응답하기 시작했습니다. 23:02 UTC에 최초 대응팀의 엔지니어들은 데이터베이스 클러스터가 예상하지 않은 상태로 구성되어 있다고 판단했습니다. Orchestrator API의 쿼리 결과는 서부 해안 데이터센터의 서버들만 표시하고 있었습니다.

### 2018년 10월 21일 23:07 UTC

이 시점에 대응팀은 추가적인 변경 내용이 적용되는 것을 막기 위해 내부 배포 도구를 수동으로 잠그기로 결정했습니다. 23:09 UTC에 [일부 장애 상황(yellow status)](https://twitter.com/githubstatus/status/1054147648930897920)을 선언했습니다. 이는 현재 상태를 ‘실제 문제 상황’으로 승격시켜 자동으로 사건 담당자에게 알림이 가도록 했습니다. 23:11 UTC에 사건 담당자가 팀에 합류하여 2분 뒤 [심각한 장애 상황(status red)](https://twitter.com/githubstatus/status/1054148705450946560)으로 변경하였습니다.

### 2018년 10월 21일 23:13 UTC

여러 데이터베이스 클러스터에 걸쳐 문제가 있음을 이 시점에서야 알게 되었습니다. 깃헙의 데이터베이스 엔지니어링 팀의 엔지니어들이 추가적으로 호출되었습니다. 그들은 각 클러스터에서 동부 해안 데이터베이스를 주 데이터베이스로 승격 시키고 구성을 복구 하기 위해 어떤 수작업이 필요한지 상황을 분석하기 시작했습니다. 이미 서부 해안의 데이터센터에 40여 분간 쓰기 작업이 이뤄졌기 때문에 작업하기가 매우 어려웠습니다. 그 뿐만 아니라 서부 해안에 복제되지 않고 동부 해안에서 복제가 막혀있는 몇 초간 작성되어 동부 해안에만 남아있는 쓰기 작업도 있었습니다.

사용자 데이터의 기밀성과 무결성 유지는 깃헙의 최우선 과제입니다. 서부 해안에만 30분 이상 기록된 사용자 데이터를 안전하게 보존하기 위해 장애 조치를 내리는 것 외에는 다른 선택이 없었습니다. 하지만 동부 해안에서 실행되는 응용 프로그램들 중 서부 해안의 MySQL 클러스터에 쓰기에 의존하는 것들은 대부분의 데이터베이스 호출에 대륙을 왕복하는 지연 시간으로 인해 제대로 대처할 수 없는 상황이었습니다. 이로 인해 많은 사용자가 서비스를 이용할 수 없게 되었습니다. 하지만 서비스 장애 상황을 확대시켜서라도 데이터 일관성을 유지하는 것이 중요하다고 믿습니다.

![잘못된 구성에서, 서부에서 동부로의 복제가 중단되고 응용 프로그램들이 트랜잭션 성능 유지를 위해 짧은 대기 시간을 기준으로 선택한 복제본에서 읽을 수 없는 상황.](https://blog.github.com/assets/img/2018-10-25-oct21-post-incident-analysis/invalid-topology.png)

### 2018년 10월 21일 23:19 UTC

데이터베이스 클러스터의 상태를 조회한 결과 푸시와 같은 메타데이터를 기록하는 작업들을 중단해야 함이 분명해졌습니다. 사용자 데이터를 위태롭게 만드는 대신 웹 훅과 깃헙 페이지 생성을 일시 중지하여 사이트 사용성을 낮추는 명확한 선택을 했습니다. 즉, 사이트 가용성과 복구에 걸리는 시간보다 데이터 무결성에 더 높은 우선 순위를 부여하는 것이 저희의 전략이었습니다.

### 2018년 10월 22일 00:05 UTC

사고 대응팀에 속한 엔지니어들은 데이터 불일치를 해결하기 위한 계획 수립과 더불어 MySQL 복원 프로시져를 구현하기 시작했습니다. 우선 백업으로부터 복원한 다음 양쪽 사이트에 있는 복제본을 동기화한 후, 데이터베이스 구성을 안정화하여 걸려 있는 작업들을 계속해서 수행하는 계획을 세웠습니다. 내부 데이터 저장 시스템을 절차에 따라 복원할 예정임을 [사용자들에게 알렸습니다](https://github.com/summernote/summernote/pull/3004).

![복구 계획의 개요. Fail forward, synchronize, fall back, then churn through backlogs before returning to green.](https://blog.github.com/assets/img/2018-10-25-oct21-post-incident-analysis/recovery-flow.png)

수 년간 4시간 단위로 MySQL 데이터 백업이 이뤄지고 있었지만, 백업은 원격에 있는 공용 퍼블릭 클라우드의 BLOB 저장 서비스에 보관되어 있었습니다. 수 테라바이트에 이르는 여러 개의 백업 데이터를 복원하느라 많은 시간이 필요했습니다. 특히 원격 백업 서비스로부터 데이터를 전송해오는데 많은 시간이 소요되었습니다. 새로 인증된 MySQL 서버로 큰 백업 파일들을 불러와 압축 해제하고 무결성 검사를 한 후 준비해서 밀어넣는데 대부분의 시간을 썼습니다. 매일 테스트 하던 작업이라 복원하는데 얼마나 시간이 걸릴지는 예상할 수 있었지만, 이 사고가 나기 전까지는 백업으로부터 전체 클러스터를 완전히 새로 구성해본 적이 없었기 때문에 지연된 복제본 등의 다른 전략에 의존하는 수 밖엔 없었습니다.

### 2018년 10월 22일 00:41 UTC

사고 영향을 받은 모든 MySQL 클러스터의 백업 프로세스가 시작되어 엔지니어들이 이를 모니터링 하고 있었습니다. 동시에 여러 팀의 엔지니어들이 데이터 손상이나 사이트 사용성을 저하시키지 않고 데이터 전송과 복원 시간을 줄일 방법을 조사하고 있었습니다.

### 2018년 10월 22일 06:51 UTC

몇몇 클러스터들은 동부 해안 데이터센터에서의 복원을 완료하고 서부 해안쪽에서의 새로운 데이터를 복제하기 시작했습니다. 대륙간 링크를 통해 쓰기 작업이 시작되느라 페이지 표시가 느려지기 시작했습니다. 대신 이 데이터베이스 클러스터에 속한 페이지를 읽을 때는 새롭게 복제된 곳에서 요청을 받아 최신의 데이터를 표시할 수 있게 되었습니다. 더 큰 데이터베이스 클러스터들은 여전히 복원중이었습니다.

팀은 서부 해안 쪽에서 직접 복원할 수 있는 방법을 찾아내어, 원격 저장소에서 다운로드 받아 복원하느라 오래 걸리던 문제를 해결하고 곧 복원을 완료할 수 있다고 확신했습니다. 구성을 정상화시키는데는 이제 복제 과정이 얼마나 오래 걸리느냐에 달려있었습니다. 원격에서 복원하던 것에 비해 선형적으로 추정할 수 있게 되었으며, 상태 페이지를 복구까지 약 2시간 정도 남은 것으로 예상한다고 [갱신](https://twitter.com/githubstatus/status/1054264047250608130)할 수 있었습니다.

### 2018년 10월 22일 07:46 UTC

깃헙은 더 많은 맥락을 전달하기 위해 [블로그 포스트](https://blog.github.com/2018-10-21-october21-incident-report)를 올렸습니다. 이를 위해 내부적으로 깃헙 페이지를 사용하고 있었는데, 이 서비스는 몇 시간 전부터 정지되어 있었으므로 블로그를 발행하기 위해 몇몇 작업을 하느라 발행이 더 늦어졌습니다. 죄송합니다. 더 빨리 알렸어야 했는데 앞으로는 이런 상황 속에서도 더 빨리 상태를 알릴 수 있도록 하겠습니다.

### 2018년 10월 22일 11:12 UTC

모든 주 데이터베이스가 동부 해안 데이터센터로 다시 설정되었습니다. 이에 쓰기 작업이 물리적으로 같은 곳의 데이터베이스 서버로 이뤄져 사이트의 반응이 훨씬 나아졌습니다. 성능은 눈에 띄게 향상되었지만 여전히 읽기 데이터베이스 노드로 복제해야 수 시간의 분량이 남아 있는 상태였습니다. 지연된 복제로 인해 서비스를 이용하는 사용자들은 일관성 없는 데이터를 보게 되었습니다. 여러 읽기 복제본에 읽기 작업을 분산시키다보니 여전히 몇 시간이나 뒤쳐진 읽기 복제본에서 요청을 처리하는 경우가 많았습니다.

실제로 복제본이 따라잡는데 필요한 예상 시간은 선형적이라기 보다는 멱함수(power delay function)에 가까웠습니다. 유럽과 미국의 근무 시간이 시작되면서 데이터베이스 클러스터로의 쓰기 요청이 많아져 복구에 걸리는 시간은 예상했던 것보다 길어졌습니다.

### 2018년 10월 22일 13:15 UTC

이제 깃헙의 최대 트래픽에 다다르고 있었습니다. 사고 대응팀에서는 어떻게 할 것인가에 대한 토론을 거쳤습니다. 복제에 걸리는 지연은 줄어들기는 커녕 증가하고 있음이 분명했습니다. 사고가 일어났을 초기에 동부 해안쪽의 공용 클라우드에 MySQL 읽기 사본을 추가해둔 상태였습니다. 이것을 사용할 수 있게 되면 더 많은 서버에 읽기 요청을 분산하기 용이해집니다. 전체적인 사용율을 낮추면 복제본이 따라잡기도 더 쉬워질 것입니다.

### 2018년 10월 22일 16:24 UTC

복제본이 동기화되는 대로 바로 원래 구성으로 돌아가게 장애 조치를 취하고 바로 지연과 가용성 문제를 다뤘습니다. 사고 시간을 줄이는 것보다 데이터 무결성을 최우선 한다는 결정하에, 백로그를 처리하는 중에도 여전히 [심각한 장애 상황(status red)](https://twitter.com/githubstatus/status/1054408042836606977)을 유지하였습니다.

### 2018년 10월 22일 16:45 UTC

이 복구 단계에서는 백로그에 의해 증가하는 부하를 다루는 것과 우리 생태계의 파트너들에 보내는 알림(notification)들, 그리고 서비스를 최대한 빠르게 100% 복원하는 것 사이에서 균형을 잡아야 했습니다. 500만개 이상의 훅 이벤트와 8만 개 이상의 페이지 생성 작업이 기다리고 있었습니다.

이 데이터 처리를 다시 시작하면서 내부적으로 설정된 제한시간(TTL)을 초과하여 취소된 20만개에 가까운 웹훅 요청을 처리하였습니다. 이를 알게되어 처리를 일단 중단하고 임시로 제한시간을 늘려 다시 작업을 진행하도록 했습니다.

상태 알림을 다시 돌리는 일이 없게끔, 백로그를 모두 처리하고 서비스가 완전히 정상적인 수준으로 명확하게 회복될 때까지 장애 상태를 유지하도록 했습니다.

### 2018년 10월 22일 23:03 UTC

밀려있던 모든 웹훅과 페이지 생성 작업이 처리되었으며 시스템 무결성과 작동이 완전히 확인되었습니다. 드디어 [정상 상태](https://twitter.com/githubstatus/status/1054508689560870912)로 돌아왔습니다.

## 앞으로 할 일

### 데이터 부정합 해결

복구 과정에서 주 사이트에서 서부 해안 사이트로 복제되지 않은 쓰기 작업을 담고 있는 MySQL 바이너리 로그(binlog)를 영향을 받은 클러스터로부터 캡춰했습니다. 서부로 복제되지 않은 총 쓰기 작업은 상대적으로 적었습니다. 가장 바쁜 클러스터에서도 영향을 받은 윈도우에 954개의 쓰기 작업이 있을 뿐이었습니다. 저희는 이러한 로그에 대한 분석을 진행하고 있으며, determining which writes can be automatically reconciled and which will require outreach to users. We have multiple teams engaged in this effort, and our analysis has already determined a category of writes that have since been repeated by the user and successfully persisted. As stated in this analysis, our primary goal is preserving the integrity and accuracy of the data you store on GitHub.

### 커뮤니케이션

In our desire to communicate meaningful information to you during the incident, we made several public estimates on time to repair based on the rate of processing of the backlog of data. In retrospect, our estimates did not factor in all variables. We are sorry for the confusion this caused and will strive to provide more accurate information in the future.

### 기술적 개선안

There are a number of technical initiatives that have been identified during this analysis. As we continue to work through an extensive post-incident analysis process internally, we expect to identify even more work that needs to happen.

  1. Adjust the configuration of Orchestrator to prevent the promotion of database primaries across regional boundaries. Orchestrator’s actions behaved as configured, despite our application tier being unable to support this topology change. Leader-election within a region is generally safe, but the sudden introduction of cross-country latency was a major contributing factor during this incident. This was emergent behavior of the system given that we hadn’t previously seen an internal network partition of this magnitude.

  2. We have accelerated our migration to a new status reporting mechanism that will provide a richer forum for us to talk about active incidents in crisper and clearer language. While many portions of GitHub were available throughout the incident, we were only able to set our status to green, yellow, and red. We recognize that this doesn’t give you an accurate picture of what is working and what is not, and in the future will be displaying the different components of the platform so you know the status of each service.

  3. In the weeks prior to this incident, we had started a company-wide engineering initiative to support serving GitHub traffic from multiple data centers in an active/active/active design. This project has the goal of supporting N+1 redundancy at the facility level. The goal of that work is to tolerate the full failure of a single data center failure without user impact. This is a major effort and will take some time, but we believe that multiple well-connected sites in a geography provides a good set of trade-offs. This incident has added urgency to the initiative.

  4. We will take a more proactive stance in testing our assumptions. GitHub is a fast growing company and has built up its fair share of complexity over the last decade. As we continue to grow, it becomes increasingly difficult to capture and transfer the historical context of trade-offs and decisions made to newer generations of Hubbers.

### 조직적 개선안

This incident has led to a shift in our mindset around site reliability. We have learned that tighter operational controls or improved response times are insufficient safeguards for site reliability within a system of services as complicated as ours. To bolster those efforts, we will also begin a systemic practice of validating failure scenarios before they have a chance to affect you. This work will involve future investment in fault injection and chaos engineering tooling at GitHub.

## 결론

We know how much you rely on GitHub for your projects and businesses to succeed. No one is more passionate about the availability of our services and the correctness of your data. We will continue to analyze this event for opportunities to serve you better and earn the trust you place in us.
