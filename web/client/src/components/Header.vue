<template>
    <div>
        <header class="header">
            <div class="title">
                АвтоДефект
            </div>
        </header>
    </div>
</template>

<script>
export default {
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Rubik:wght@700&display=swap');

.header {
    height: 100px;
    background: #FFF;
    box-shadow: 0px 10px 40px 5px rgba(19, 142, 255, 0.05);
}

.title {
    display:inline-block;
    width: 211px;
    height: 20px;
    margin-top: 40px;
    margin-left: 34px;
    color: #138EFF;
    font-family: Rubik;
    font-size: 32px;
    font-style: normal;
    font-weight: 700;
    line-height: 20px;
    transition: 2.0s;
    animation: title 2.0s 1;
    animation-fill-mode: forwards;
}

@keyframes title {
    0% {
        opacity: 0;
        transform: translateY(-20px);
    }
    100% {
        opacity: 1;
    }
}

</style>