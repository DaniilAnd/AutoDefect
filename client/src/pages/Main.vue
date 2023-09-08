<template>
  <div class="container-fluid">
    <div class="row content">

            <div class="col">
                <div class="row">
                    <div class="col search_panel">
                        <div class="search_item">
                            <label for="city">Город</label><br>
                            <select class="form-select" name="city" id="city">
                                <option value="all">Все города</option>
                                <option value="spb">Санкт-Петербург</option>
                                <option value="msk">Москва</option>
                            </select>
                        </div>
                        <div class="search_item">
                            <label for="state">Состояние</label><br>
                            <select class="form-select" name="state" id="state">
                                <option value="all">Любое</option>
                                <option value="ok">Допустимое</option>
                                <option value="critical">Критичное</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-6 map_panel" id="map">
                        <YandexMap :coordinates="center">
                            <div 
                                v-for="report in reports"
                                :key="report.id"
                            >
                                <YandexMarker :coordinates="[report['gps_coordinates']['x'], report['gps_coordinates']['y']]" :marker-id="report.id">
                                    <template #component>
                                    <CustomBalloon :value="report" />
                                    </template>
                                </YandexMarker>
                            </div>
                        </YandexMap>
                    </div>
                </div>
                <div class="row">
                    <div class="col list_panel">
                        <div class="list_logo">Дефекты на дороге</div>
                        <table id="table_container" class="table"></table>
                    </div>
                </div>
            </div>

            <div class="col pit_panel">
                <div class="row">
                    <div class="col">
                        <div class="row">
                            <div class="pit_date col" id="pit_date"></div>
                            <div class="pit_state col" id="pit_state"></div>
                        </div>
                        <div class="row mt-2">
                            <div class="col pit_city" id="pit_city"></div>
                            <div class="col pit_street" id="pit_street"></div>
                        </div>
                        <div class="row">
                            <div class="col pit_coords" id="pit_coords"></div>
                        </div>
                        <div 
                            class="row"
                            :hidden="img_data.length == 0 ? true : false"
                        >
                            <div class="row mt-3 mb-2">
                                <div class="col pit_header" >Параметры ямы</div>
                            </div>
                            <div class="row">
                                <div class="col pit_desc" >Ширина</div>
                                <div class="col pit_desc" >15см</div>
                            </div>
                            <div class="row">
                                <div class="col pit_desc" >Длина ямы</div>
                                <div class="col pit_desc" >25см</div>

                            </div>
                            <div class="row">
                                <div class="col pit_desc" >Глубина ямы</div>
                                <div class="col pit_desc" >3см</div>
                            </div>
                        </div>
                    </div>
                    <div class="col" style="text-align: end;">
                        <img 
                            class="pit_image" 
                            :src="img_data" 
                            :hidden="img_data.length == 0 ? true : false" 
                        >
                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { yandexMap, yandexMarker } from 'vue-yandex-maps';
import CustomBalloon from '@/components/UI/CustomBallon.vue';
    
export default {
    components: {
        CustomBalloon,
        yandexMap, yandexMarker,
    },
    data() {
        return {
            data: {
                'Фото': ['https://img2.fedpress.ru/thumbs/800/2022/08/2404/d0aa206869a44e06c90b12f48338ebb6.jpg', 'https://img2.fedpress.ru/thumbs/800/2022/08/2404/d0aa206869a44e06c90b12f48338ebb6.jpg', 'https://img2.fedpress.ru/thumbs/800/2022/08/2404/d0aa206869a44e06c90b12f48338ebb6.jpg', 'https://img2.fedpress.ru/thumbs/800/2022/08/2404/d0aa206869a44e06c90b12f48338ebb6.jpg'],
            },
            reports: [],
            center: [],
            img_data: '',
            cols_ru: ['Дата', 'Город', 'Улица', 'Состояние'],
            cols_en: ['time_escalation', 'city', 'street', 'state'],
        }
    },
    methods: {
        async showImage(image_path) {
            const url = `http://localhost:8000/api/image?image_path=${image_path}`;
            const method = "GET";
            const response = await fetch(url, { method })

            const imageData = await response.blob();
            this.img_data = URL.createObjectURL(imageData);
        },
        showActive(data) {
            this.center = [data['gps_coordinates']['x'], data['gps_coordinates']['y']]
            document.getElementById('pit_coords').innerHTML = `${data['gps_coordinates']['x']}, ${data['gps_coordinates']['y']}`;
            document.getElementById('pit_city').innerHTML = `${data['city']}`;
            document.getElementById('pit_street').innerHTML = `${data['street']}`;
            document.getElementById('pit_date').innerHTML = data['time_escalation'].split('T')[0];
            document.getElementById('pit_state').innerHTML = data['state'];
            this.showImage(data['image_path'])
        },
        showTable(data) {
            let cells = '<tbody>';  
            for (let ncol=0; ncol<this.cols_ru.length; ncol++) {
                    let col = this.cols_ru[ncol]
                    cells += `<td>${col}</td>`;
            }
            table_container.innerHTML += cells + '</tbody>'

            let nRows = data.length;
            for (let row=0; row<nRows; row++) {
                let tbody = document.createElement('tbody');
                let cells = '';
                for (let ncol=0; ncol<this.cols_en.length; ncol++) {
                    let col = this.cols_en[ncol]
                    if (col === 'time_escalation') {
                        cells += `<td>${data[row][col].split('T')[0]}</td>`;
                    }
                    else {
                        cells += `<td>${data[row][col]}</td>`;
                    }
                }
                let onclickF = ()=>{
                    this.showActive(data[row]);
                }
                tbody.innerHTML += cells;
                tbody.addEventListener('click', onclickF);
                table_container.appendChild(tbody);
            }
        },
        async fetchReports() {
            try {
                const response = await axios.get('http://localhost:8000/api/reports');
                this.reports = response.data.data;
            } catch (e) {
                alert('Ошибка')
            }
        },
    },
    async mounted() {
        await this.fetchReports();
        this.center = [this.reports[0]["gps_coordinates"]["x"], this.reports[0]["gps_coordinates"]["y"]]
        this.showTable(this.reports);
    }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rubik&display=swap');

.container-fluid {
    font-family: 'Rubik', sans-serif;
    background-color: #EFF6FE;
}

.content {
    padding-top: 20px;
    padding-left: 40px;
    padding-right: 40px;
}

.logo {
    position: absolute;
    top: 50%;
    transform: translate(0,-60%);
}

.search_panel {
    height: 400px;
    background-color: white;
    border-radius: 15px;
    margin: 20px;
    padding: 30px;
}

.map_panel {
    height: 400px;
    background-color: white;
    border-radius: 15px;
    margin: 20px;
    padding: 0px;
    position: relative;
}

.pit_panel {
    height: 700px;
    background-color: white;
    border-radius: 15px;
    margin: 20px;
    padding: 30px;
}

.list_logo {
    font-family: Rubik;
    font-size: 20px;
    font-weight: bold;
}

.list_panel {
    background-color: white;
    border-radius: 15px;
    margin: 20px;
    padding: 30px;
}

.search_item {
    width: 100%;
    font-family: rubik;
    font-size: 16px;
    font-weight: bold;
    margin-bottom: 20px;
}

.pit_image {
    object-fit: cover;
    width: 400px;
    height: 400px;
    border-radius: 15px;
}

.pit_date {
    color: #138EFF;
    font-weight: bold;
}

.pit_state {
    text-align: end;
    font-weight: bold;
}

.pit_coords {
    font-size: 15px;
}

.pit_header {
    font-size: 18px;
    font-weight: bold;
}

.pit_desc {
    font-size: 16px;
}

select {
    width: 100%;
}

[class*="copyright"] {
    display: none !important;
}

[class*="grounds-pane"] {
    display: none !important;
}

#map > ymaps {
    border-radius: 15px;
    overflow: hidden;
}

tbody:nth-of-type(even) { 
    background: #EFF6FE; 
}

tbody:nth-of-type(odd) { 
    background: white; 
}

td {
    padding: 10px
}

table {
    width: 100%;
    font-size: 14px;
    font-family: rubik;
}

.yandex-container {
    height: 100%;
    width: 100%;
}


</style>